"""Local Markdown retrieval for the drilling knowledge copilot."""
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass(frozen=True)
class Chunk:
    text: str
    source: str


class KnowledgeBase:
    """Build a small in-memory TF-IDF index from Markdown reference files."""

    def __init__(self, knowledge_dir: Path, chunk_words: int = 180, overlap_words: int = 30):
        self.chunks = self._load_chunks(knowledge_dir, chunk_words, overlap_words)
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([chunk.text for chunk in self.chunks]) if self.chunks else None

    @staticmethod
    def _load_chunks(directory: Path, chunk_words: int, overlap_words: int) -> list[Chunk]:
        chunks: list[Chunk] = []
        step = max(1, chunk_words - overlap_words)
        for path in sorted(directory.glob("*.md")):
            words = path.read_text(encoding="utf-8").split()
            for start in range(0, len(words), step):
                text = " ".join(words[start : start + chunk_words]).strip()
                if text:
                    chunks.append(Chunk(text=text, source=path.name))
        return chunks

    def search(self, question: str, limit: int = 4) -> list[dict]:
        if not self.chunks or self.matrix is None:
            return []
        scores = cosine_similarity(self.vectorizer.transform([question]), self.matrix).ravel()
        ranked = scores.argsort()[::-1][:limit]
        return [
            {"text": self.chunks[index].text, "source": self.chunks[index].source, "score": round(float(scores[index]), 4)}
            for index in ranked
            if scores[index] > 0
        ]
