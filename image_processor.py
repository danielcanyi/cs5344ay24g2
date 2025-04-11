"""
Process images from scraped content:
1. Download images from URLs
2. Tag them with relevant terms from the document
3. Save processed images and metadata
"""
import os
import json
import requests
from typing import Dict, List
import constants
from PIL import Image
from io import BytesIO
import hashlib

from collections import defaultdict
import math
import re


# Load global IDF values (from key_terms.py output)
idf_path = os.path.join(constants.DIR_KEY_TERMS, "global_idf.json")
with open(idf_path, 'r', encoding='utf-8') as f:
    GLOBAL_IDF = json.load(f)


def process_images(test_mode=False, max_docs=2) -> None:
    """
    Main function to process images, test_mode allows restricting number of documents
    """
    os.makedirs(constants.DIR_IMAGES, exist_ok=True)

    for domain_name in [
        constants.SITE_NAME_TRAVELERFOLIO,
        constants.SITE_NAME_THESMARTLOCAL,
        constants.SITE_NAME_ALVINOLOGY,
        constants.SITE_NAME_THEOCCASIONALTRAVELLER
    ]:
        process_domain_images(domain_name, test_mode=test_mode, max_docs=max_docs)


def process_domain_images(domain_name: str, test_mode: bool = False, max_docs: int = 2) -> None:
    json_dir = os.path.join(constants.DIR_JSON, domain_name)
    if not os.path.exists(json_dir):
        return

    count = 0
    for filename in os.listdir(json_dir):
        if not filename.endswith('.json'):
            continue

        filepath = os.path.join(json_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            doc = json.loads(f.read())
            process_document_images(doc, domain_name, filename)
            count += 1
            if test_mode and count >= max_docs:
                break


def process_document_images(doc: Dict, domain_name: str, filename: str) -> None:
    """
    Process all images from a single document
    """
    title = doc.get(constants.DOC_KEY_TITLE, '')
    key_terms = doc.get(constants.DOC_KEY_KEY_TERMS, [])
    content = doc.get(constants.DOC_KEY_CONTENT, [])

    # Create directory for this document's images
    doc_image_dir = os.path.join(constants.DIR_IMAGES, domain_name, filename.replace('.json', ''))
    os.makedirs(doc_image_dir, exist_ok=True)

    # Process each image in the content
    for item in content:
        if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) == constants.DOC_CONTENT_ITEM_TYPE_IMG:
            img_src = item.get(constants.DOC_CONTENT_ITEM_KEY_SRC)
            if img_src:
                try:
                    # Download and save image
                    img_data = download_image(img_src)
                    if img_data:
                        # Generate unique filename
                        img_filename = generate_image_filename(img_src)
                        img_path = os.path.join(doc_image_dir, img_filename)
                        
                        # Save image
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                        
                        # Create metadata file
                        metadata = {
                            'original_url': img_src,
                            'document_title': title,
                            'key_terms': extract_local_terms_tf_idf(content, item),
                            'filename': img_filename
                        }
                        metadata_path = os.path.join(doc_image_dir, f"{img_filename}.json")
                        with open(metadata_path, 'w', encoding='utf-8') as f:
                            json.dump(metadata, f, ensure_ascii=False, indent=2)
                        
                        print(f"Processed image: {img_path}")
                except Exception as e:
                    print(f"Error processing image {img_src}: {str(e)}")

def download_image(url: str) -> bytes:
    """
    Download an image from a URL
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error downloading image {url}: {str(e)}")
        return None

def generate_image_filename(url: str) -> str:
    """
    Generate a unique filename for an image based on its URL
    """
    # Create a hash of the URL to ensure uniqueness
    url_hash = hashlib.md5(url.encode()).hexdigest()
    
    # Get file extension from URL
    ext = os.path.splitext(url)[1]
    if not ext:
        ext = '.jpg'  # Default extension if none found
    
    return f"{url_hash}{ext}"

def extract_local_terms_tf_idf(content: List[Dict], image_item: Dict, window: int = 3, max_terms: int = 10) -> List[str]:
    """
    Extracts nearby terms and ranks them using TF-IDF, based on global IDF.
    """
    try:
        index = content.index(image_item)
    except ValueError:
        return []

    # Gather nearby text
    nearby_text = []
    for i in range(max(0, index - window), min(len(content), index + window + 1)):
        item = content[i]
        if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) in {
            constants.DOC_CONTENT_ITEM_TYPE_TEXT,
            constants.DOC_CONTENT_ITEM_TYPE_H2,
            constants.DOC_CONTENT_ITEM_TYPE_H3
        }:
            nearby_text.append(item.get(constants.DOC_CONTENT_ITEM_KEY_TEXT, "").lower())

    # Tokenize, remove stopwords
    words = []
    for text in nearby_text:
        words.extend([
            word for word in re.split(r'\W+', text)
            if word and word not in constants.NLTK_STOPWORDS
        ])

    if not words:
        return []

    # Term Frequencies (TF)
    tf_counts = defaultdict(int)
    for word in words:
        tf_counts[word] += 1

    max_tf = max(tf_counts.values())
    tf_idf_scores = {}

    # Compute TF × IDF for each word
    for term, freq in tf_counts.items():
        tf = freq / max_tf
        idf = GLOBAL_IDF.get(term, math.log(3949))  # Fallback IDF
        tf_idf_scores[term] = tf * idf

    # Return top N terms
    sorted_terms = sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)
    return [term for term, _ in sorted_terms[:max_terms]]

if __name__ == "__main__":
    process_images() 