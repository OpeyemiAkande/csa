from qdrant_client import QdrantClient

# from qdrant_client.http import models
from fastembed import TextEmbedding
from agents import Agent, Runner
from app_state import require_state
from model.csa import QueryRequest, QueryResponse, QueryDetails


async def process_query(request: QueryRequest) -> QueryResponse:  # type: ignore
    collection_name: str = "docs_embeddings"

    try:
        state = require_state()
        client: QdrantClient = state.client  # type: ignore
        embedding_model: TextEmbedding = state.embedding_model  # type: ignore
        processor_agent: Agent = state.processor_agent  # type: ignore

        # 1. Embed query and search
        query_embedding = list(embedding_model.embed([request.query]))[0]
        search_response = client.query_points(
            collection_name=collection_name,
            query=query_embedding.tolist(),
            limit=3,
            with_payload=True,
        )
        search_results = (
            search_response.points if hasattr(search_response, "points") else []
        )
        if not search_results:
            raise Exception("No relevant documents found in the vector database")

        # 2. Build context
        context = "Based on the following documentation:\n\n"
        for result in search_results:
            payload = result.payload
            if not payload:
                continue
            url = payload.get("url", "Unknown URL")
            content = payload.get("content", "")
            context += f"From {url}:\n{content}\n\n"
        context += f"\nUser Question: {request.query}\n\n"
        context += (
            "Please provide a clear, concise answer that can be easily spoken out loud."
        )

        # 3. Processor agent (text reasoning)
        processor_result = await Runner.run(processor_agent, context)
        processor_response = processor_result.final_output

        # 6. Return structured result
        return {
            "status": "success",
            "text_response": processor_response,
            "sources": [
                r.payload.get("url", "Unknown URL") for r in search_results if r.payload
            ],
            "query_details": QueryDetails(
                vector_size=len(query_embedding),
                results_found=len(search_results),
                collection_name=collection_name,
            ),
        }  # type: ignore

    except Exception as e:
        raise e
