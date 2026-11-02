# Evaluation contract
Provide documents as an ID-to-text object and queries as an array of objects with unique id, text and nonempty relevant document IDs. k is a positive integer. Each query has equal weight in macro recall. Rank only positive scores, breaking ties by document ID. BM25 uses k1=1.2 and b=0.75. No relevance labels enter either scoring function.
