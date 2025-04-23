import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from recommender import TravelRecommender, load_documents
import constants
import csv

K = 5  # Number of recommendations to compare

def generate_fused_strings(documents, use_images):
    recommender = TravelRecommender(documents, use_images=use_images)
    fused_strings = []
    for doc in tqdm(documents, desc=f"Extracting features (images={'on' if use_images else 'off'})"):
        text_features = recommender.extract_text_features(doc)
        image_features = recommender.extract_image_features(doc) if use_images else {'image_terms': [], 'image_context': []}
        fused = recommender.fuse_features(text_features, image_features)
        fused_strings.append(' '.join(fused.keys()))
    return fused_strings

def run_comparison(documents, k=5, output_csv="clip_image_ablation_results.csv"):
    recommender = TravelRecommender(documents, use_images=True)
    print("Generating feature strings...")
    fused_text = generate_fused_strings(documents, use_images=False)
    fused_image = generate_fused_strings(documents, use_images=True)

    # Get raw image feature counts
    image_features = recommender.extract_image_features(documents[i])
    num_image_terms = len(image_features.get("image_terms", []))
    num_image_context = len(image_features.get("image_context", []))


    print("Vectorizing...")
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3))
    vec_text = vectorizer.fit_transform(fused_text)
    vec_image = vectorizer.transform(fused_image)

    results = []

    print("\nComparing recommendations (text vs image-enhanced)...")
    for i in range(len(documents)):
        sim_text = cosine_similarity(vec_text[i], vec_text).flatten()
        sim_image = cosine_similarity(vec_image[i], vec_image).flatten()

        top_k_text = np.argsort(sim_text)[::-1][1:k+1]
        top_k_image = np.argsort(sim_image)[::-1][1:k+1]

        overlap = set(top_k_text).intersection(set(top_k_image))
        jaccard = len(overlap) / len(set(top_k_text).union(top_k_image))

        titles_text_only = [
            documents[idx].get(constants.DOC_KEY_TITLE, "Untitled").strip()
            for idx in top_k_text
        ]
        titles_with_images = [
            documents[idx].get(constants.DOC_KEY_TITLE, "Untitled").strip()
            for idx in top_k_image
        ]
        new_titles = [
            documents[idx].get(constants.DOC_KEY_TITLE, "Untitled").strip()
            for idx in set(top_k_image) - set(top_k_text)
        ]

        results.append({
            "Doc Index": i + 1,
            "Title": documents[i].get(constants.DOC_KEY_TITLE, "No Title").strip(),
            "URL": documents[i].get("original_url", "N/A"),
            "Overlap": len(overlap),
            "Jaccard": round(jaccard, 2),
            "Recs from Text Only": "; ".join(titles_text_only),
            "Recs from Text + Image": "; ".join(titles_with_images),
            "New Recs from Image Features": "; ".join(new_titles),
            "Image Terms Count": num_image_terms,
            "Image Context Count": num_image_context
        })

    # Save to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "Doc Index", "Title", "URL", "Overlap", "Jaccard",
            "Recs from Text Only", "Recs from Text + Image", "New Recs from Image Features",
            "Image Terms Count", "Image Context Count"
        ]


        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\nResults saved to {output_csv}")



if __name__ == "__main__":
    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")
    run_comparison(documents, k=K)
