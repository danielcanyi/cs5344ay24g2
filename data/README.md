# Directory structure:

## Raw Scraped HTML
```
html/<domain-name>/<single-scraped-page-name>.html
e.g.
├── html
│   ├── alvinology
│   │   ├── 100-doraemon-secret-gadget-expo-johor-bahru-city-square.html
│   │   ├── 10-authentic-experiences-try-touring-vietnam.html

```

## HTML pages converted into json docs
```
json/<domain-name/<single-scraped-page-name>.json
e.g.
├── json
│   ├── alvinology
│   │   ├── 100-doraemon-secret-gadget-expo-johor-bahru-city-square.json
│   │   ├── 10-authentic-experiences-try-touring-vietnam.json
```

## json docs with terms added
```
with_key_terms/<doc-number>.json
e.g.
└── with_key_terms
    ├── 0.json
    ├── 1000.json
    ├── 1001.json
    ├── 1002.json
    ├── 1003.json
    ├── 1004.json
    ├── 1005.json
    ├── 1006.json
    ├── 1007.json
    ├── 1008.json
    ├── 1009.json

```

### Saved counts for terms
`with_key_terms/global_term_doc_counts.json`

### Saved IDFs
`with_key_terms/global_idf.json`

Do not commit the scraped files into the git repo.
