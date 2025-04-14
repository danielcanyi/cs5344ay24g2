SITE_NAME_TRAVELERFOLIO = "travelerfolio"
SITE_NAME_THESMARTLOCAL = "thesmartlocal"
SITE_NAME_ALVINOLOGY = "alvinology"
SITE_NAME_THEOCCASIONALTRAVELLER = "theoccasionaltraveller"
SITE_NAME_THEWORLDTRAVELGUY = "theworldtravelguy"
SITE_NAME_ASIATOURS = "asiatours"

DIR_HTML = "data/html"
DIR_JSON = "data/json"
DIR_KEY_TERMS = "data/with_key_terms"
DIR_IMAGES = "data/images"


"""
{
    title: <main title>
    content: [
        {
            type: <img | h2 | h3 | text>,
            text: <text if any>,
            src: <src if any>
        }
    ],
    "key_terms": [ <term> ]
}
"""

DOC_KEY_TITLE = "title"
DOC_KEY_CONTENT = "content"
DOC_KEY_KEY_TERMS = "key_terms"

DOC_CONTENT_ITEM_KEY_TYPE = "type"
DOC_CONTENT_ITEM_KEY_TEXT = "text"
DOC_CONTENT_ITEM_KEY_SRC = "src"

DOC_CONTENT_ITEM_TYPE_IMG = "img"
DOC_CONTENT_ITEM_TYPE_H2 = "h2"
DOC_CONTENT_ITEM_TYPE_H3 = "h3"
DOC_CONTENT_ITEM_TYPE_TEXT = "text"

NLTK_STOPWORDS = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves",
                  "you", "your", "yours", "yourself", "yourselves", "he",
                  "him", "his", "himself", "she", "her", "hers", "herself",
                  "it", "its", "itself", "they", "them", "their", "theirs",
                  "themselves", "what", "which", "who", "whom", "this",
                  "that", "these", "those", "am", "is", "are", "was", "were",
                  "be", "been", "being", "have", "has", "had", "having", "do",
                  "does", "did", "doing", "a", "an", "the", "and", "but", "if",
                  "or", "because", "as", "until", "while", "of", "at", "by",
                  "for", "with", "about", "against", "between", "into",
                  "through", "during", "before", "after", "above", "below",
                  "to", "from", "up", "down", "in", "out", "on", "off", "over",
                  "under", "again", "further", "then", "once", "here", "there",
                  "when", "where", "why", "how", "all", "any", "both", "each",
                  "few", "more", "most", "other", "some", "such", "no", "nor",
                  "not", "only", "own", "same", "so", "than", "too", "very",
                  "s", "t", "can", "will", "just", "don", "should", "now"]
