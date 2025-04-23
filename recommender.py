"""
Multi-modal recommender system that combines text and image features
for travel article recommendations.
"""
import os
import json
import argparse
import hashlib
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import constants
from image_processor import extract_local_terms_tf_idf

class TravelRecommender:
    def __init__(self, documents: List[Dict], use_images: bool = True, num_processes: Optional[int] = None):
        """
        Initialize the recommender with a list of documents
        Args:
            documents: List of document dictionaries
            use_images: Whether to use image features in recommendations
            num_processes: Number of processes to use for parallel processing
        """
        self.documents = documents
        self.use_images = use_images
        self.num_processes = num_processes or max(1, cpu_count() - 1)
        self.feature_weights = {
            'title_terms': 1.0,    # Reduced from 1.5
            'key_terms': 1.0,
            'location_terms': 1.0, # Reduced from 1.2
            'image_terms': 2.0 if use_images else 0.0,   
            'image_context': 1.5 if use_images else 0.0   
        }
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 3)
        )
        self.clusters = None
        self.feature_vectors = None
        self.location_whitelist = self._load_location_whitelist()
        self.location_words = self._preprocess_locations()

    def _load_location_whitelist(self) -> set:
        """Load location whitelist from file"""
        whitelist_path = os.path.join('data', 'country_city_whitelist', 'location_whitelist.txt')
        locations = set()
        try:
            with open(whitelist_path, 'r', encoding='utf-8') as f:
                for line in f:
                    location = line.strip().lower()
                    if location and len(location) > 2:  # Skip very short locations
                        locations.add(location)
        except Exception as e:
            print(f"Warning: Could not load location whitelist: {str(e)}")
        return locations

    def _preprocess_locations(self) -> Dict[str, set]:
        """Preprocess locations into a word-based lookup dictionary"""
        word_locations = defaultdict(set)
        for location in self.location_whitelist:
            words = location.split()
            for word in words:
                if len(word) > 2:  # Skip very short words
                    word_locations[word].add(location)
        return dict(word_locations)

    def _extract_location_terms(self, doc: Dict) -> List[str]:
        """
        Extract location-related terms from document using optimized matching
        """
        locations = set()
        text_parts = []
        
        # Collect all text parts to search
        title = doc.get(constants.DOC_KEY_TITLE, '').lower()
        if title:
            text_parts.append(title)
        
        for item in doc.get(constants.DOC_KEY_CONTENT, []):
            if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) in [
                constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                constants.DOC_CONTENT_ITEM_TYPE_H2,
                constants.DOC_CONTENT_ITEM_TYPE_H3
            ]:
                text = item.get(constants.DOC_CONTENT_ITEM_KEY_TEXT, '').lower()
                if text:
                    text_parts.append(text)
        
        # Check key terms
        key_terms = doc.get(constants.DOC_KEY_KEY_TERMS, [])
        for term in key_terms:
            if isinstance(term, list):
                term = ' '.join(str(t) for t in term)
            term = str(term).lower()
            if term:
                text_parts.append(term)
        
        # Search for locations in all text parts
        for text in text_parts:
            words = text.split()
            for word in words:
                if len(word) <= 2:
                    continue
                if word in self.location_words:
                    for location in self.location_words[word]:
                        if location in text:
                            locations.add(location)
        
        return list(locations)

    def extract_text_features(self, doc: Dict) -> Dict:
        """
        Extract features from document text, keeping only top 5 terms
        """
        features = {
            'key_terms': [],
            'title_terms': [],
            'location_terms': [],
            'content_terms': []
        }
        
        # Get key terms and keep top 5
        key_terms = doc.get(constants.DOC_KEY_KEY_TERMS, [])
        if isinstance(key_terms, list):
            # Flatten nested lists
            flat_terms = []
            for term in key_terms:
                if isinstance(term, list):
                    flat_terms.extend(term)
                else:
                    flat_terms.append(term)
            # Keep top 5 unique terms
            features['key_terms'] = list(set(flat_terms))[:5]
        
        # Get title terms and keep top 5
        title = doc.get(constants.DOC_KEY_TITLE, '')
        title_terms = self._extract_title_terms(title)
        features['title_terms'] = title_terms[:5]
        
        # Get location terms and keep top 5
        location_terms = self._extract_location_terms(doc)
        features['location_terms'] = location_terms[:5]
        
        # Get content terms and keep top 5
        content_terms = self._extract_content_terms(doc.get(constants.DOC_KEY_CONTENT, []))
        features['content_terms'] = content_terms[:5]
        
        return features

    def extract_image_features(self, doc: Dict) -> Dict:
        """
        Extract features from document images, keeping only top 5 terms
        """
        features = {
            'image_terms': [],
            'image_context': []
        }
        
        image_terms = []
        context_terms = []
        image_count = 0
        
        
        for item in doc.get(constants.DOC_KEY_CONTENT, []):
            if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) == constants.DOC_CONTENT_ITEM_TYPE_IMG:
                image_count += 1
                # Get image metadata
                img_src = item.get(constants.DOC_CONTENT_ITEM_KEY_SRC)
                if img_src:
                    img_metadata = self._load_image_metadata(img_src)
                    if img_metadata:
                        terms = img_metadata.get('key_terms', [])
                        if terms:
                            image_terms.extend(terms)
                        else:
                            print("No terms found in metadata")
                    
                    # Extract context terms
                    context = extract_local_terms_tf_idf(
                        doc.get(constants.DOC_KEY_CONTENT, []),
                        item,
                        window=5
                    )
                    if context:
                        context_terms.extend(context)
                    else:
                        print("No context terms found")
        
        # Keep top 5 unique terms for each
        features['image_terms'] = list(set(image_terms))[:5]
        features['image_context'] = list(set(context_terms))[:5]
        
        print(f"\nTotal images processed: {image_count}")
        print(f"Final image terms: {features['image_terms']}")
        print(f"Final context terms: {features['image_context']}")
        
        return features

    def fuse_features(self, text_features: Dict, image_features: Dict) -> Dict:
        """
        Combine text and image features with appropriate weighting
        """
        fused_features = defaultdict(float)
        
        # Combine and weight text features
        for term in text_features['key_terms']:
            fused_features[str(term)] += self.feature_weights['key_terms']
        for term in text_features['title_terms']:
            fused_features[str(term)] += self.feature_weights['title_terms']
        for term in text_features['location_terms']:
            fused_features[str(term)] += self.feature_weights['location_terms']
        
        # Combine and weight image features
        for term in image_features['image_terms']:
            fused_features[str(term)] += self.feature_weights['image_terms']
        for term in image_features['image_context']:
            fused_features[str(term)] += self.feature_weights['image_context']
        
        # Print top terms for debugging
        if self.use_images:
            print("\nTop Terms:")
            print("Key Terms:", text_features['key_terms'])
            print("Title Terms:", text_features['title_terms'])
            print("Location Terms:", text_features['location_terms'])
            print("Image Terms:", image_features['image_terms'])
            print("Image Context:", image_features['image_context'])
        
        return dict(fused_features)

    def _extract_title_terms(self, title: str) -> List[str]:
        """
        Extract terms from document title
        """
        # Remove special characters and split into words
        words = title.lower().split()
        return [word for word in words if word not in constants.NLTK_STOPWORDS]

    def _extract_content_terms(self, content: List[Dict]) -> List[str]:
        """
        Extract terms from document content
        """
        terms = []
        for item in content:
            if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) in [
                constants.DOC_CONTENT_ITEM_TYPE_TEXT,
                constants.DOC_CONTENT_ITEM_TYPE_H2,
                constants.DOC_CONTENT_ITEM_TYPE_H3
            ]:
                text = item.get(constants.DOC_CONTENT_ITEM_KEY_TEXT, '')
                words = text.lower().split()
                terms.extend([word for word in words if word not in constants.NLTK_STOPWORDS])
        return terms

    def _load_image_metadata(self, img_src: str) -> Optional[Dict]:
        """
        Load image metadata saved in CLIP-generated JSON format.
        Only attempt for local image paths.
        """
        if not img_src or img_src.startswith("http://") or img_src.startswith("https://"):
            return None  # Skip web URLs entirely

        try:
            relative_path = os.path.relpath(img_src, constants.DIR_IMAGES)
        except ValueError:
            return None  # Skip if relpath fails

        metadata_path = os.path.join("data/clip_images", relative_path + ".json")

        if not os.path.exists(metadata_path):
            return None

        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                return metadata if metadata.get("key_terms") else None
        except Exception as e:
            print(f"Error loading CLIP metadata from {metadata_path}: {e}")
            return None



    def prepare_features(self):
        """
        Prepare feature vectors for all documents using parallel processing
        """
        print("Preparing features...")
        # Split documents into chunks for parallel processing
        chunk_size = max(1, len(self.documents) // self.num_processes)
        doc_chunks = [self.documents[i:i + chunk_size] 
                     for i in range(0, len(self.documents), chunk_size)]
        
        # Process chunks in parallel with progress bar
        with Pool(self.num_processes) as pool:
            # Map: Extract features from each document chunk
            feature_chunks = list(tqdm(
                pool.imap(self._process_doc_chunk, doc_chunks),
                total=len(doc_chunks),
                desc="Processing document chunks"
            ))
        
        # Reduce: Combine all feature strings
        print("Combining features...")
        all_features = []
        for chunk in tqdm(feature_chunks, desc="Combining chunks"):
            all_features.extend(chunk)
        
        # Convert to feature vectors
        print("Creating feature vectors...")
        self.feature_vectors = self.vectorizer.fit_transform(all_features)

    def cluster_documents(self, eps: float = 0.3, min_samples: int = 5):
        """
        Cluster documents based on fused features
        """
        if self.feature_vectors is None:
            self.prepare_features()
        
        print("Clustering documents...")
        # Perform clustering
        clustering = DBSCAN(
            eps=eps,
            min_samples=min_samples,
            metric='cosine',
            n_jobs=self.num_processes  # Use parallel processing for clustering
        )
        
        self.clusters = clustering.fit_predict(self.feature_vectors)
        return self.clusters

    def recommend_similar(self, query_doc: Dict, k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Recommend similar documents based on fused features
        """
        if self.feature_vectors is None:
            self.prepare_features()
        if self.clusters is None:
            self.cluster_documents()
        
        # Get query document index
        query_idx = self.documents.index(query_doc)
        
        # Find documents in same cluster
        query_cluster = self.clusters[query_idx]
        cluster_indices = [i for i, c in enumerate(self.clusters) if c == query_cluster and i != query_idx]
        
        if not cluster_indices:
            return []
        
        print("Calculating similarities...")
        # Calculate similarities in parallel with progress bar
        with Pool(self.num_processes) as pool:
            similarities = list(tqdm(
                pool.starmap(
                    self._calculate_similarity,
                    [(query_idx, idx) for idx in cluster_indices]
                ),
                total=len(cluster_indices),
                desc="Calculating similarities"
            ))
        
        # Combine with documents and sort
        recommendations = list(zip(
            [self.documents[i] for i in cluster_indices],
            similarities
        ))
        return sorted(recommendations, key=lambda x: x[1], reverse=True)[:k]

    def _process_doc_chunk(self, doc_chunk: List[Dict]) -> List[str]:
        """
        Process a chunk of documents to extract features
        Args:
            doc_chunk: List of documents to process
        Returns:
            List of feature strings for the documents
        """
        chunk_features = []
        for doc in doc_chunk:
            text_features = self.extract_text_features(doc)
            image_features = self.extract_image_features(doc)
            fused_features = self.fuse_features(text_features, image_features)
            chunk_features.append(' '.join(fused_features.keys()))
        return chunk_features

    def _calculate_similarity(self, query_idx: int, doc_idx: int) -> float:
        """
        Calculate similarity between two documents
        Args:
            query_idx: Index of the query document
            doc_idx: Index of the document to compare with
        Returns:
            Similarity score between the documents
        """
        return cosine_similarity(
            self.feature_vectors[query_idx],
            self.feature_vectors[doc_idx]
        )[0][0]

def load_documents(limit: Optional[int] = None) -> List[Dict]:
    """
    Load documents from the with_key_terms directory
    Args:
        limit: Maximum number of documents to load (None for all)
    """
    documents = []
    if not os.path.exists(constants.DIR_KEY_TERMS):
        print(f"Error: Directory {constants.DIR_KEY_TERMS} does not exist")
        return documents
        
    for filename in os.listdir(constants.DIR_KEY_TERMS):
        if filename.endswith('.json') and filename not in ['global_term_doc_counts.json', 'global_idf.json']:
            if limit and len(documents) >= limit:
                break
            filepath = os.path.join(constants.DIR_KEY_TERMS, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:
                        print(f"Warning: Empty file {filename}")
                        continue
                    try:
                        doc = json.loads(content)
                        documents.append(doc)
                    except json.JSONDecodeError as e:
                        print(f"Warning: Invalid JSON in {filename}: {str(e)}")
                        continue
            except Exception as e:
                print(f"Warning: Error reading {filename}: {str(e)}")
                continue
    
    if not documents:
        print("Warning: No valid documents were loaded")
    else:
        print(f"Successfully loaded {len(documents)} documents")
    
    return documents

def analyze_documents_with_images(documents: List[Dict]) -> List[Dict]:
    """
    Analyze and return documents that have images
    Returns:
        List of documents with images, sorted by number of images
    """
    docs_with_images = []
    for doc in documents:
        image_count = len([item for item in doc.get(constants.DOC_KEY_CONTENT, []) 
                          if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) == constants.DOC_CONTENT_ITEM_TYPE_IMG])
        if image_count > 0:
            docs_with_images.append((doc, image_count))
    
    # Sort by number of images (descending)
    docs_with_images.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, _ in docs_with_images]

def print_document_info(doc: Dict):
    """Print basic information about a document"""
    print(f"\nTitle: {doc.get(constants.DOC_KEY_TITLE, 'No title')}")
    
    # Handle nested lists in key terms
    key_terms = doc.get(constants.DOC_KEY_KEY_TERMS, [])
    if key_terms:
        # Flatten nested lists
        flat_terms = []
        for term in key_terms:
            if isinstance(term, list):
                flat_terms.extend(term)
            else:
                flat_terms.append(term)
        print(f"Key Terms: {', '.join(str(term) for term in flat_terms)}")
    else:
        print("Key Terms: None")
    
    # Count images and print image sources
    image_count = 0
    print("\nImages:")
    for item in doc.get(constants.DOC_KEY_CONTENT, []):
        if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) == constants.DOC_CONTENT_ITEM_TYPE_IMG:
            image_count += 1
            img_src = item.get(constants.DOC_CONTENT_ITEM_KEY_SRC, 'No source')
            print(f"  {image_count}. {img_src}")
    print(f"Total Images: {image_count}")

def calculate_metrics(recommendations_with_images: List[Tuple[Dict, float]], 
                     recommendations_without_images: List[Tuple[Dict, float]]) -> Dict:
    """
    Calculate comparison metrics between recommendations with and without image features
    """
    # Get document titles for comparison
    titles_with_images = {doc.get(constants.DOC_KEY_TITLE) for doc, _ in recommendations_with_images}
    titles_without_images = {doc.get(constants.DOC_KEY_TITLE) for doc, _ in recommendations_without_images}
    
    # Calculate overlap
    overlap = titles_with_images.intersection(titles_without_images)
    overlap_ratio = len(overlap) / len(titles_with_images) if titles_with_images else 0
    
    # Calculate average similarity scores
    avg_similarity_with_images = np.mean([sim for _, sim in recommendations_with_images]) if recommendations_with_images else 0
    avg_similarity_without_images = np.mean([sim for _, sim in recommendations_without_images]) if recommendations_without_images else 0
    
    return {
        'overlap_count': len(overlap),
        'overlap_ratio': overlap_ratio,
        'avg_similarity_with_images': avg_similarity_with_images,
        'avg_similarity_without_images': avg_similarity_without_images,
        'similarity_difference': avg_similarity_with_images - avg_similarity_without_images
    }

def compare_recommendations(documents: List[Dict], query_doc: Dict, k: int = 5):
    """Compare recommendations with and without image features"""
    print("\n=== Comparing Recommendations ===")
    print("\nQuery Document:")
    print_document_info(query_doc)
    
    # With images
    print("\n=== Recommendations with Image Features ===")
    recommender_with_images = TravelRecommender(documents, use_images=True)
    recommender_with_images.prepare_features()
    recommender_with_images.cluster_documents()
    recommendations_with_images = recommender_with_images.recommend_similar(query_doc, k)
    
    for doc, similarity in recommendations_with_images:
        print(f"\nSimilarity: {similarity:.2f}")
        print_document_info(doc)
    
    # Without images
    print("\n=== Recommendations without Image Features ===")
    recommender_no_images = TravelRecommender(documents, use_images=False)
    recommender_no_images.prepare_features()
    recommender_no_images.cluster_documents()
    recommendations_no_images = recommender_no_images.recommend_similar(query_doc, k)
    
    for doc, similarity in recommendations_no_images:
        print(f"\nSimilarity: {similarity:.2f}")
        print_document_info(doc)
    
    # Calculate and display metrics
    metrics = calculate_metrics(recommendations_with_images, recommendations_no_images)
    print("\n=== Comparison Metrics ===")
    print(f"Number of overlapping recommendations: {metrics['overlap_count']}")
    print(f"Overlap ratio: {metrics['overlap_ratio']:.2%}")
    print(f"Average similarity with images: {metrics['avg_similarity_with_images']:.3f}")
    print(f"Average similarity without images: {metrics['avg_similarity_without_images']:.3f}")
    print(f"Similarity difference: {metrics['similarity_difference']:.3f}")

def interactive_mode(documents: List[Dict]):
    """Run the recommender in interactive mode"""
    # First, analyze documents with images
    docs_with_images = analyze_documents_with_images(documents)
    print(f"\nFound {len(docs_with_images)} documents with images out of {len(documents)} total documents")
    
    while True:
        print("\n=== Interactive Recommender ===")
        print("1. List documents with images")
        print("2. Compare recommendations for a document")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print("\nDocuments with Images:")
            for i, doc in enumerate(docs_with_images):
                image_count = len([item for item in doc.get(constants.DOC_KEY_CONTENT, []) 
                                 if item.get(constants.DOC_CONTENT_ITEM_KEY_TYPE) == constants.DOC_CONTENT_ITEM_TYPE_IMG])
                print(f"{i+1}. {doc.get(constants.DOC_KEY_TITLE, 'No title')} ({image_count} images)")
        
        elif choice == "2":
            try:
                doc_idx = int(input("\nEnter document number to analyze: ")) - 1
                if 0 <= doc_idx < len(docs_with_images):
                    k = int(input("Enter number of recommendations to show (default 5): ") or 5)
                    compare_recommendations(documents, docs_with_images[doc_idx], k)
                else:
                    print("Invalid document number")
            except ValueError:
                print("Please enter a valid number")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid choice")

def main():
    parser = argparse.ArgumentParser(description='Travel Article Recommender System')
    parser.add_argument('--limit', type=int, help='Limit number of documents to process')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--compare', type=int, help='Document index to compare recommendations for')
    parser.add_argument('--k', type=int, default=5, help='Number of recommendations to show')
    
    args = parser.parse_args()
    
    # Load documents
    print("Loading documents...")
    documents = load_documents(args.limit)
    print(f"Loaded {len(documents)} documents")
    
    if args.interactive:
        interactive_mode(documents)
    elif args.compare is not None:
        if 0 <= args.compare < len(documents):
            compare_recommendations(documents, documents[args.compare], args.k)
        else:
            print("Invalid document index")
    else:
        # Default behavior: compare first document
        compare_recommendations(documents, documents[0], args.k)

if __name__ == "__main__":
    main()
