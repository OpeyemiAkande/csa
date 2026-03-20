import os
from typing import Any, Optional, List, Dict
import uuid
from datetime import datetime
import time
from firecrawl import Firecrawl  # type: ignore
from qdrant_client import QdrantClient
from qdrant_client.http import models
from fastembed import TextEmbedding


def crawl_documentation(  # type: ignore
    firecrawl_api_key: str, url: str, output_dir: Optional[str] = None
):
    firecrawl = Firecrawl(api_key=firecrawl_api_key)
    pages = []

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    response: Any = firecrawl.crawl(  # type: ignore
        url, limit=10, scrape_options={"formats": ["markdown", "html"]}  # type: ignore
    )

    while True:
        for page in response.data or []:  # type: ignore
            # Each page is a Document object
            content = getattr(page, "markdown", None) or getattr(page, "html", "")  # type: ignore
            metadata = getattr(page, "metadata", {}) or {}  # type: ignore
            source_url = getattr(metadata, "source_url", "")

            if output_dir and content:
                filename = f"{uuid.uuid4()}.md"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

            pages.append(  # type: ignore
                {
                    "content": content,
                    "url": source_url,
                    "metadata": {
                        "title": getattr(metadata, "title", ""),
                        "description": getattr(metadata, "description", ""),
                        "language": getattr(metadata, "language", "en"),
                        "crawl_date": datetime.now().isoformat(),
                    },
                }
            )
        next_url = response.next  # type: ignore

        if not next_url:
            break

        response = firecrawl.get(next_url)  # type: ignore
        time.sleep(1)

    return pages  # type: ignore


def store_embeddings(
    client: QdrantClient,
    embedding_model: TextEmbedding,
    pages: List[Dict],  # type: ignore
    collection_name: str,
) -> None:
    for page in pages:  # type: ignore
        embedding = list(embedding_model.embed([page["content"]]))[0]  # type: ignore
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding.tolist(),
                    payload={
                        "content": page["content"],
                        "url": page["url"],
                        **page["metadata"],
                    },
                )
            ],
        )
