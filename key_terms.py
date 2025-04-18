"""
Extract the important terms within all the 'text' paragraphs and place push
them into a top-level array field with name `constants.DOC_KEY_KEY_TERMS`

New files saved into another data directory
"""
import os
from collections.abc import Iterable
import json
import re
import math
from typing import List, Set, Tuple
import constants
from constants import (
    DOC_KEY_TITLE,
    DOC_KEY_CONTENT,
    DOC_KEY_KEY_TERMS,

    DOC_CONTENT_ITEM_KEY_TYPE,
    DOC_CONTENT_ITEM_KEY_TEXT,

    DOC_CONTENT_ITEM_TYPE_H2,
    DOC_CONTENT_ITEM_TYPE_H3,
    DOC_CONTENT_ITEM_TYPE_TEXT,
    NLTK_STOPWORDS
)

NUM_TOP_TERMS = 200


# term: how many documents it appears in
_global_term_doc_counts = {}
_global_idf = {}

WHITELIST_PATH = "data/country_city_whitelist/location_whitelist.txt"

def _load_location_whitelist() -> Set[str]:
    if not os.path.exists(WHITELIST_PATH):
        return set()
    with open(WHITELIST_PATH, "r", encoding="utf-8") as f:
        return set(line.strip().lower() for line in f if line.strip())

def add_key_terms() -> None:
    doc_index = 0

    # First pass, collect document counts, needed for TF.IDF
    for doc in _read_src_files():
        doc_index += 1
        print("[Key Terms] First pass: Processing doc {}".format(
            str(doc_index)))
        _term_and_tfs = []
        for term, tf in _tf(_text_terms_from_doc(doc)):
            term_key = _dict_key_for_term(term)
            if term_key not in _global_term_doc_counts:
                _global_term_doc_counts[term_key] = 0
            _global_term_doc_counts[term_key] = \
                _global_term_doc_counts[term_key] + 1

            _term_and_tfs.append((term, tf))

        doc["_term_and_tfs"] = _term_and_tfs
        # Write to disk first
        _save_doc(str(doc_index), doc)
        print("[Key Terms] First pass: Doc {} saved".format(str(doc_index)))

    # Save global stats
    _save_doc("global_term_doc_counts", _global_term_doc_counts)
    print("[Key Terms] IDF calculation")
    # Calculate idfs
    for key in _global_term_doc_counts:
        idf = math.log((doc_index / _global_term_doc_counts[key]), 2)
        _global_idf[key] = idf
    _save_doc("global_idf", _global_idf)
    print("[Key Terms] IDF done")

    """
    # For skipping first pass,
    # comment the blocks above and uncomment this block
    doc_index = 3949
    with open(
        constants.DIR_KEY_TERMS + "/global_idf.json",
        'r', encoding='utf-8'
    ) as f:
        _global_idf = json.loads(f.read())
    """
    # Load location whitelist
    location_whitelist = _load_location_whitelist()

    # Second pass, calculate tf.idf and filter
    for i in range(doc_index):
        curr_filename = i + 1
        print("[Key Terms] Second pass: Processing doc {}".format(
            str(curr_filename)))
        filepath = "{}/{}.json".format(
            constants.DIR_KEY_TERMS, str(curr_filename))

        key_terms = []
        with open(filepath, 'r', encoding='utf-8') as f:
            doc = json.loads(f.read())
            term_and_tf_idf = []
            for term, tf in doc.get("_term_and_tfs"):
                term_key = _dict_key_for_term(term)
                idf = _global_idf.get(term_key)
                tf_idf = tf * idf
                term_and_tf_idf.append((term, tf_idf))
            sorted_term_and_tf_idf = sorted(
                term_and_tf_idf, key=lambda tup: tup[1], reverse=True)
            

            # Select top NUM_TOP_TERMS
            top_terms = []
            for j in range(min(NUM_TOP_TERMS, len(sorted_term_and_tf_idf))):
                top_terms.append(sorted_term_and_tf_idf[j][0])

            # Extract all text from title and content
            text_blob = doc.get(DOC_KEY_TITLE, "") + " "
            for para in doc.get(DOC_KEY_CONTENT, []):
                text_blob += " " + para.get(DOC_CONTENT_ITEM_KEY_TEXT, "")

            # Tokenize and filter location hits
            text_blob_words = set(_text_to_words(text_blob))

            location_hits = []
            for word in text_blob_words:
                if word in location_whitelist:
                    location_hits.append([word])

            # Combine top_terms + location_hits while deduplicating
            seen_keys = set()
            combined_terms = []

            for term in top_terms + location_hits:
                key = _dict_key_for_term(term)
                if key not in seen_keys:
                    seen_keys.add(key)
                    combined_terms.append(term)

            # Store in document
            doc[DOC_KEY_KEY_TERMS] = combined_terms

            _save_doc(str(curr_filename), doc)

        print("[Key Terms] Second pass: Doc {} saved".format(
            str(curr_filename)))

    print("[Key Terms] Top {} terms for each Doc saved".format(
        str(NUM_TOP_TERMS)))
    print("[Key Terms] Done")


def _text_terms_from_doc(doc: dict) -> Iterable[List[str]]:

    for term in _terms_from_text(doc.get(DOC_KEY_TITLE)):
        yield term

    for para in doc.get(DOC_KEY_CONTENT):
        if para.get(DOC_CONTENT_ITEM_KEY_TYPE) in [
            DOC_CONTENT_ITEM_TYPE_TEXT,
            DOC_CONTENT_ITEM_TYPE_H2,
            DOC_CONTENT_ITEM_TYPE_H3
        ]:
            for term in _terms_from_text(para.get(DOC_CONTENT_ITEM_KEY_TEXT)):
                yield term


def _terms_from_text(text: str) -> Iterable[List[str]]:
    words = list(_filter_stopwords(_text_to_words(text)))
    for shingle in _shingles_from_words(words, k=1):
        yield shingle
    for shingle in _shingles_from_words(words, k=2):
        yield shingle
    for shingle in _shingles_from_words(words, k=3):
        yield shingle


def _shingles_from_words(words: List[str], k: int) -> Iterable[List[str]]:
    for start in range(len(words)):
        yield words[start:(start + k)]


def _tf(terms: Iterable[Set[str]]) -> Iterable[Tuple[List[str], float]]:
    # TODO: change data structure of freqs if needed
    freqs = {}
    for term in terms:
        key = _dict_key_for_term(term)
        if key not in freqs:
            freqs[key] = 0
        freqs[key] = freqs[key] + 1

    if not freqs:
        return []

    max_freq = max([freqs[key] for key in freqs])

    for key in freqs:
        yield (_term_from_dict_key(key), freqs[key] / max_freq)


def _dict_key_for_term(s: List[str]) -> str:
    """Modify if needed"""
    return ",".join(s)


def _term_from_dict_key(key: str) -> List[str]:
    return key.split(",")


def _filter_stopwords(words: Iterable[str]) -> Iterable[str]:
    return filter(lambda word: word not in NLTK_STOPWORDS, words)


def _text_to_words(text: str) -> Iterable[str]:
    return [word for word in re.split(r'\W+', text.lower()) if word.isalpha()]


def _read_src_files() -> Iterable[dict]:
    for filepath in _get_filepaths(constants.DIR_JSON):
        with open(filepath, 'r', encoding='utf-8') as f:
            yield json.loads(f.read())


def _read_key_term_files() -> Iterable[dict]:
    for filepath in _get_filepaths(constants.DIR_KEY_TERMS):
        with open(filepath, 'r', encoding='utf-8') as f:
            yield json.loads(f.read())


def _get_filepaths(parent_path: os.PathLike) -> Iterable[os.PathLike]:
    for root, dirs, files in os.walk(parent_path):
        for name in files:
            yield os.path.join(root, name)


def _save_doc(name: str, doc: dict) -> None:
    """`name` should not have extensions e.g. .json"""
    os.makedirs(constants.DIR_KEY_TERMS, exist_ok=True)
    path = "{}/{}".format(constants.DIR_KEY_TERMS, name + ".json")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(doc))


if __name__ == "__main__":
    add_key_terms()
