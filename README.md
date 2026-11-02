# Retrieval Bench

Compare a token-overlap baseline with BM25 before changing the retrieval stage of a local document assistant. The report shows which labeled queries gain or lose relevant documents at a fixed cutoff.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

This in-memory lexical benchmark uses Unicode word tokens and case folding. No stemming, embeddings or model calls. Results on the synthetic corpus illustrate ranking behavior only.

## Resumen en español

Evalúa dos rankings sobre las mismas consultas etiquetadas. El informe muestra qué documentos recupera cada método y dónde cambia la cobertura.
