# Association Rule Mining for Travel Site Data

This project processes JSON files containing scraped travel site data to mine frequent itemsets and association rules based on the text content of each page. The code extracts tokens from the titles and body text of each JSON file, applies filtering to remove stopwords and irrelevant terms, converts the text data into transactions, and then uses the Apriori algorithm and association rule mining to discover relationships between tokens (which may represent travel activities).

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [TODO][#todo]

## Overview

This code performs the following steps:
1. **Load JSON files:** Recursively read all JSON files from a specified base directory.
2. **Tokenize Text Data:** Extract word tokens from the `title` and `content` fields of each JSON record.
3. **Filtering:** Remove stopwords (both standard English and domain-specific stopwords) and non-alphabetic tokens.
4. **Frequency Filtering:** Count token frequencies across transactions and filter out tokens that appear less than a specified threshold.
5. **Transaction Encoding:** Convert the list of tokenized transactions into a one-hot encoded DataFrame.
6. **Frequent Itemset Mining:** Run the Apriori algorithm to extract frequent itemsets based on a minimum support threshold.
7. **Association Rules:** Generate association rules from the frequent itemsets based on a confidence threshold.
8. **Saving Results:** Output the frequent itemsets, sorted frequent itemsets, and association rules to CSV files.

## Requirements

- **Python 3**
- **Libraries:**
  - `json`
  - `re`
  - `os`
  - `pandas`
  - `mlxtend`
  - `nltk`
  - `glob` (optional, but useful for file operations)
- **NLTK Stopwords:**
  - The code downloads the English stopwords from NLTK. (Make sure to have an internet connection for the first run.)

# TODO

Itemsets generated do not provide much activity-related words. It's mostly travel-related words such as "experience", "food", "explore", etc. 

Method 1: Manually construct target activities and look for direct matches.
Method 2: Use NER to extract activity phrases
Method 3: Topic modelling to identify activity-focused topics 



