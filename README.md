# cs5344ay24g2
cs5344 ay 24/25 group 2
Original proposal: `CS5344 Project_AY24-25_Sem2 for group 2.pdf`

# Setup
```
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

# Scraping, saves html data

Warning: Scraped data can be huge

```
source venv/bin/activate
python3 scrape.py
```

# Converting scraped html data into json
Requires scraped html data
```
source venv/bin/activate
python3 html_to_json.py
```

# Extracting and saving key terms
Requires scraped and converted json data
```
source venv/bin/activate
python3 key_terms.py
```

# Processing and downloading images
Requires json data with key terms
```
source venv/bin/activate
python3 image_processor.py
```
This script will:
1. Download images from URLs found in JSON files
2. Save images with unique hashed filenames
3. Create metadata JSON files containing:
   - Original URL
   - Document title
   - Key terms from the document
   - Generated filename

# Counting images and folders
To get statistics about the downloaded images:
```
source venv/bin/activate
python3 count_images.py
```
This script provides:
- Total number of images downloaded
- Total number of folders created
- Number of empty folders

# Notes:
- Articles scraped: `5549`
- 14 Apr: 
  - added 335 articles from theworldtravelguy
  - added 100 articles from asiatours
- 18 Apr:
  - added 444 articles from asialegend
  - added 28 articles from nomadicmatt
  - added 126 articles from wanderlush
  - added 560 articles from asiakingtravel
## Terms
- 1-shingle, 2-shingle and 3-shingle used for terms
  - Reason: attraction names are sometimes up to 3 words
- Used TF.IDF for finding key terms within documents
  - Text from headings and titles treated the same as normal text; TF.IDF robust enough to find significance of words even when hierarchy is lost.

- Tried using a threshold to only accept terms with a TF.IDF above some threshold, but does not produce a good balance of terms per document
  - TF.IDF Threshold: 0.5, Total terms: 1930585, Avg / doc: 488.8794631552292, Min / doc: 2, Max / doc: 2466
  - Switched to taking the top n terms based on TF.IDF for each document instead

### Taking the top n terms with the highest TF.IDF
See `TF_IDF_SAMPLES.md`
Analysis: n=200 seems the sweet spot because at around n=300 some articles start returning non-travel-activity related words to do with their promotions

## Problems:
- Articles sometimes reference some other location
  - Ex: article about Phuket, "Quiet beach is definitely a far cry from Patong"
  - No real solution yet
- Many Ad Articles: articles that have large proportions of content not relevant to what one does in a country
  - Perhaps Clustering can help: discard very small clusters
  - Perhaps the recommendation / frequent items would not find the content of these articles frequent anyway
- Country / location names are too common across documents and would hence have a low IDF
  - Make a search for location names in text separate from TF.IDF

# Possible issue for Windows 10/11 Pro "FileNotFoundError: [Errno 2] No such file or directory: " 

Windows Long Paths Setup (Windows 10/11 Pro) 
If you're using Windows 10/11 Pro, you need to enable long paths to handle deep directory structures and long filenames. Follow these steps:

1. Press `Windows + R` to open the Run dialog
2. Type `gpedit.msc` and press Enter to open the Local Group Policy Editor
3. Navigate to: `Computer Configuration > Administrative Templates > System > Filesystem`
4. Find and double-click on `Enable Win32 long paths`
5. Select `Enabled` and click `OK`
6. Restart your computer for the changes to take effect

## TODO:
- [High] Presentation PPT
  - Person in charge tries to understand what everyone's been doing and creates the slides to their understanding
- [High] Process and Tag Images:
  - Downloading and transforming
  - Tagging with the terms from the same document
    - Or even better, with the terms nearest to its position in the document
- [High] Include specially searched location / country keywords into terms regardless of TF.IDF
- [High] Frequent Itemsets: discover frequent itemsets
  - May need to scrape more sites, because each site may only mention one activity once
- [Medium] Find association rules based on terms, depends on finding Frequent itemsets
- [Medium] Explore using recommender systems - content-based filtering
  - If not feasible, investigate and report why
- [Low] Change code to using mapreduce
- [Low] Similar documents: Use the minhashing and LSH of terms to find jaccard similarity between documents
- [Low] Clustering: Use document similarity to do hierarchical clustering


# Data Sources:
- Stopwords from Python NLTK library: https://www.nltk.org/
- Scraped sites:
    - https://travelerfolio.com/
    - https://thesmartlocal.com/
    - https://alvinology.com/
    - https://theoccasionaltraveller.net/
    - https://theworldtravelguy.com/
    - https://www.asiatours.com/
    - https://www.asiakingtravel.com/
    - https://wander-lush.org
    - https://www.nomadicmatt.com/
    - https://asialegend.travel/

- Country/ City Whitelist : https://github.com/ToniCifre/all-countries-and-cities-json/tree/master

---
data will be scraped/generated into `data/`
