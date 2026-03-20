from typing import Optional
from dataclasses import dataclass
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from agents import Agent


@dataclass
class AppState:
    client: Optional[QdrantClient] = None
    embedding_model: Optional[TextEmbedding] = None
    processor_agent: Optional[Agent] = None


state = AppState()


def require_state() -> AppState:
    if state.client is None or state.embedding_model is None:
        raise RuntimeError(
            "AppState not initialized. Ensure FastAPI startup completed."
        )
    return state
