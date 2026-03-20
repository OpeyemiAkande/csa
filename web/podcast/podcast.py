from fastapi import APIRouter, HTTPException
import service.podcast.podcast as service
from model.podcast import PodcastRequest, PodcastResponse
from typing import Any
from error import Missing

router = APIRouter(prefix="/podcast")


@router.post("", status_code=201, response_model=PodcastResponse)
async def generate_podcast(request: PodcastRequest):
    try:
        return await service.generate_podcast_service(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{podcast_id}")
async def get_one_podcast(podcast_id: str) -> dict[str, Any]:
    try:
        return await service.get_one_podcast(podcast_id)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
