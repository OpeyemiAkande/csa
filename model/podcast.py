# schemas/podcast.py
from pydantic import BaseModel

# from typing import Any


class PodcastRequest(BaseModel):
    blog_url: str


class PodcastResponse(BaseModel):
    message: str


class PodcastMetadata(BaseModel):
    _id: str
    blog_url: str
    audio_data: bytes
    audio_format: str
