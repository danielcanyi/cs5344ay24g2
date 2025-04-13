import json
import re
import os
from glob import glob
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from collections import Counter
import nltk
from nltk.corpus import stopwords

def load_json_files():
    nltk.download('stopwords')
    standard_stopwords = set(stopwords.words('english'))
    domain_stopwords = {
        'first', 'time', 'like', 'one', 'also', 'activities', 'new', 'see', 
        'try', 'next', 'get', 'come', 'make', 'things', 'people', 'good', 'go', 
        'high', 'home', 'visit', 'tour', 'trip'  # add/remove words based on domain knowledge
    }
    all_stopwords = standard_stopwords.union(domain_stopwords)

    # Load JSON files
    base_directory = r"C:\Users\limmi\Desktop\Ming En\Masters\Modules\Sem 3\CS5344\Project\cs5344ay24g2\data\travel_site_jsons\json"
    data = []
    for root, dirs, files in os.walk(base_directory):
        print("Loading from {}".format(root))
        for filename in files:
            if filename.lower().endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf=8') as file:
                    try:
                        record = json.load(file)
                        data.append(record)
                    except json.JSONDecodeError:
                        print(f"Error reading {file_path}, skipping this file")


    print("Number of JSON files loaded: {}".format(len(data)))
    return data

def get_word_tokens(data):
    travel_activities = {
        "hiking", "snorkeling", "scuba", "diving", "skiing", "kayaking",
        "rafting", "shopping", "sightseeing", "camping", "surfing",
        "ziplining", "trekking", "climbing", "fishing", "safari"
    }

    # Get tokens from each title and content
    tokens = []
    print("Getting Word tokens")
    for record in data:
        page = []

        if 'title' in record:
            title_tokens = re.findall(r'\b\w+\b', record['title'].lower())
            title_tokens = [token for token in title_tokens if token.isalpha() and token not in all_stopwords]
            page.extend(title_tokens)
            # print(title_tokens)
        
        if 'content' in record:
            for content_item in record['content']:
                if content_item.get('type') == 'text' and 'text' in content_item:
                    text_tokens = re.findall(r'\b\w+\b', content_item['text'].lower())
                    text_tokens = [token for token in text_tokens if token.isalpha() and token not in all_stopwords]
                    page.extend(text_tokens)
                    # print(text_tokens)
        
        page = list(set(page))
        tokens.append(page)

    # Count all tokens across transactions
    all_tokens = [token for transaction in tokens for token in transaction]
    token_counts = Counter(all_tokens)
    print("Number of words: {}".format(len(token_counts)))

    # Set a threshold for the minimum number of appearances (adjust as needed)
    min_token_frequency = 3

    # Filter tokens in each transaction
    tokens = [
        [token for token in transaction if token_counts[token] >= min_token_frequency]
        for transaction in tokens
    ]
    return tokens

def get_itemsets(tokens, save=True):
    # Convert list of transactions into one-hot encoded DataFrame
    print("Converting tokens")
    te = TransactionEncoder()
    te_ary = te.fit(tokens).transform(tokens)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # Apply Apriori Algorithm to extract frequent itemsets
    print("Getting frequent itemsets")
    min_sp = 0.1
    freq_itemsets = apriori(df, min_support=min_sp, use_colnames=True)

    single_item_itemsets = freq_itemsets[freq_itemsets['itemsets'].apply(lambda x: len(x) == 1)]
    most_frequent_activities = single_item_itemsets.sort_values(by='support', ascending=False)
    print("Most frequent activities")
    print(most_frequent_activities)

    sorted_itemsets = freq_itemsets.sort_values(by='support', ascending=False)
    print("sorted itemsets")
    print(sorted_itemsets)

    # Get association rules
    rules = association_rules(freq_itemsets, metric="confidence", min_threshold=0.7)

    if save:
        freq_itemsets.to_csv(r"output/frequent_itemsets.csv", index=False)
        most_frequent_activities.to_csv(r"output/most_frequent_itemsets.csv", index=False)
        sorted_itemsets.to_csv(r"output/sorted_itemsets.csv", index=False)
        rules.to_csv(r"output/assoc_rules.csv", index=False)

if __name__ == "__main__":
    # Comment and uncomment
    data = load_json_files()
    tokens = get_word_tokens(data)
    get_itemsets(tokens, True)
