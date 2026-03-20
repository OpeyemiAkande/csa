from motor.motor_asyncio import AsyncIOMotorClient
from qdrant_client import QdrantClient
from fastembed import TextEmbedding
from qdrant_client.http.models import Distance, VectorParams
from beanie import init_beanie  # type: ignore
from settings import Settings

import logging


# from app.models.user import User

app_settings = Settings()  # type: ignore
logger = logging.getLogger("uvicorn.error")
client = AsyncIOMotorClient(app_settings.mongo_uri)  # type: ignore


async def ping_mongo_db_server():
    try:
        await client.admin.command("ping")  # type: ignore
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e


def setup_qdrant_collection(
    qdrant_url: str, qdrant_api_key: str, collection_name: str = "docs_embeddings"
):
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    embedding_model = TextEmbedding()
    test_embedding = list(embedding_model.embed(["test"]))[0]
    embedding_dim = len(test_embedding)

    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE),
        )
        logger.info("Qdrant setup complete!")
    except Exception as e:
        if "already exists" not in str(e):
            logger.error(f"Error setting up Qdrant: {e}")
            raise e

    return client, embedding_model
