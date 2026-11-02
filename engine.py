import math
import re
from collections import Counter


def tokens(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return re.findall(r"\w+", text.casefold())


def ranked(scores, k):
    return sorted((key for key in scores if scores[key] > 0),
                  key=lambda key: (-scores[key], key))[:k]


def evaluate(data):
    docs = {key: Counter(tokens(text)) for key, text in data["documents"].items()}
    k = data["k"]
    if type(k) is not int or k < 1 or not docs or not data["queries"]:
        raise ValueError("supply documents, queries and positive integer k")
    lengths = {key: counts.total() for key, counts in docs.items()}
    mean_length = sum(lengths.values()) / len(docs)
    frequency = Counter(word for counts in docs.values() for word in counts)
    seen = set()
    rows = []
    for query in data["queries"]:
        qid = query["id"]
        relevant = set(query["relevant"])
        if qid in seen or not relevant or not relevant.issubset(docs):
            raise ValueError("duplicate query or invalid relevance labels")
        seen.add(qid)
        terms = set(tokens(query["text"]))
        overlap, weighted = {}, {}
        for key, counts in docs.items():
            matches = sorted(terms.intersection(counts))
            overlap[key] = len(matches)
            score = 0.0
            for term in matches:
                idf = math.log1p((len(docs) - frequency[term] + 0.5) / (frequency[term] + 0.5))
                norm = 1.2 * (0.25 + 0.75 * lengths[key] / mean_length)
                score += idf * counts[term] * 2.2 / (counts[term] + norm)
            weighted[key] = score
        row = {"id": qid}
        for name, scores in [("overlap", overlap), ("bm25", weighted)]:
            ids = ranked(scores, k)
            row[name] = {"ids": ids, "recall": len(relevant.intersection(ids)) / len(relevant)}
        row["delta"] = row["bm25"]["recall"] - row["overlap"]["recall"]
        rows.append(row)
    return {"k": k, "queries": rows, "macro_recall": {
        name: sum(row[name]["recall"] for row in rows) / len(rows) for name in ("overlap", "bm25")}}
