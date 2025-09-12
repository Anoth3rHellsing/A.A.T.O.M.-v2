from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import faiss
import numpy as np
import openai

EMBED_MODEL = "text-embedding-ada-002"
EMBED_DIM = 1536


class MemoryManager:
    """Store and search text memories using OpenAI embeddings and FAISS."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self.index_path = self.path / "index.bin"
        self.meta_path = self.path / "meta.json"

        if self.index_path.exists() and self.meta_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.meta_path, "r", encoding="utf-8") as f:
                self.meta: List[Dict[str, Any]] = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(EMBED_DIM)
            self.meta = []

    def _embed(self, text: str) -> np.ndarray:
        """Return the ada-002 embedding for the given text."""
        response = openai.Embedding.create(model=EMBED_MODEL, input=[text])
        return np.array(response["data"][0]["embedding"], dtype=np.float32)

    def add(self, text: str, meta: Dict[str, Any]) -> None:
        """Add text and metadata to the index."""
        embedding = self._embed(text)
        self.index.add(np.array([embedding], dtype=np.float32))
        self.meta.append({"text": text, "meta": meta})

        faiss.write_index(self.index, str(self.index_path))
        with open(self.meta_path, "w", encoding="utf-8") as f:
            json.dump(self.meta, f, ensure_ascii=False, indent=2)

    def search(self, query: str, k: int = 3) -> List[Tuple[str, Dict[str, Any], float]]:
        """Return the top *k* memories closest to *query*."""
        if self.index.ntotal == 0:
            return []
        embedding = self._embed(query)
        distances, indices = self.index.search(np.array([embedding], dtype=np.float32), k)

        results: List[Tuple[str, Dict[str, Any], float]] = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < 0 or idx >= len(self.meta):
                continue
            entry = self.meta[idx]
            results.append((entry["text"], entry["meta"], float(dist)))
        return results
