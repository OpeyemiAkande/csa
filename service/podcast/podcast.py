import uuid
from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
import base64
from typing import Any

# from agno.run.response import RunResponse
from agno.utils.audio import write_audio_to_file  # type: ignore
from model.podcast import PodcastRequest, PodcastResponse, PodcastMetadata
from data.podcast.podcast import save_podcast_metadata, get_one_podcast


async def generate_podcast_service(request: PodcastRequest) -> PodcastResponse:
    agent = Agent(
        name="Blog to Podcast Agent",
        agent_id="blog_to_podcast_agent",  # type: ignore
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            ElevenLabsTools(
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                model_id="eleven_multilingual_v2",
                target_directory="audio_generations",
            ),
            FirecrawlTools(),
        ],
        description="You are an AI agent that can generate audio using the ElevenLabs API.",
        instructions=[
            "When the user provides a blog URL:",
            "1. Use FirecrawlTools to scrape the blog content",
            "2. Create a concise summary of the blog content that is NO MORE than 2000 characters long",
            "3. Make it engaging and conversational",
            "4. Convert the summary to audio",
        ],
        markdown=True,
        debug_mode=True,
    )

    podcast = agent.run(f"Convert the blog content to a podcast: {request.blog_url}")  # type: ignore

    if not podcast.audio:
        raise ValueError("No audio generated")

    # Get audio as Base64 (MP3)
    audio_base64 = podcast.audio[0].base64_audio  # type: ignore

    # Convert to binary for storage
    audio_binary = base64.b64decode(audio_base64)  # type: ignore

    # Save in MongoDB
    podcast_id = str(uuid.uuid4())

    metadata = PodcastMetadata(
        _id=podcast_id,
        blog_url=request.blog_url,
        audio_data=audio_binary,
        audio_format="mp3",
    )

    await save_podcast_metadata(metadata)

    return PodcastResponse(message="Podcast generated successfully")


async def get_one(podcast_id: str) -> dict[str, Any]:
    podcast = await get_one_podcast(podcast_id)
    return podcast
