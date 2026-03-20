# data/podcast_repository.py
from db.database import mongo_database
from model.podcast import PodcastMetadata
from bson import ObjectId
from typing import Any
from error import Missing
import base64


async def save_podcast_metadata(metadata: PodcastMetadata) -> str:
    db = mongo_database()
    result = await db.podcasts.insert_one(metadata.model_dump())

    return str(result.inserted_id)


async def get_one_podcast(podcast_id: str) -> dict[str, Any]:
    db = mongo_database()

    podcast = await db.podcasts.find_one(
        {"_id": ObjectId(podcast_id) if ObjectId.is_valid(podcast_id) else None}
    )

    if not podcast:
        raise Missing(msg=f"Podcast not found")

    podcast["_id"] = str(podcast["_id"])
    podcast["audio_data"] = base64.b64encode(podcast["audio_data"]).decode("utf-8")
    return podcast


async def update_podcast():
    pass
