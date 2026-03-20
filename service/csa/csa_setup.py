from env_setup import app_settings
from app_state import require_state
from db.ingestion import store_embeddings, crawl_documentation  # type: ignore
from agents import Agent
import os

# import logging

# logger = logging.getLogger("uvicorn.error")


def injest_data():
    state = require_state()
    pages = crawl_documentation(  # type: ignore
        firecrawl_api_key=app_settings.firecrawl_api_key, url=app_settings.doc_url
    )

    print(f"Successfully crawled {len(pages)}")  # type: ignores

    if not pages:
        print("Some Error occured")

    store_embeddings(
        client=state.client,  # type: ignore
        embedding_model=state.embedding_model,  # type: ignore
        pages=pages,  # type: ignore
        collection_name="docs_embeddings",
    )


def setup_agents(openai_api_key: str):
    os.environ["OPENAI_API_KEY"] = openai_api_key

    processor_agent = Agent(
        name="Documentation Processor",
        instructions="""You are a helpful documentation assistant. Your task is to:
        1. Analyze the provided documentation content
        2. Answer the user's question clearly and concisely
        3. Include relevant examples when available
        4. Cite the source URLs when referencing specific content
        5. Keep responses natural and conversational
        6. Format your response in a way that's easy to speak out loud""",
        model="gpt-4o",
    )

    return processor_agent
