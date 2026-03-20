from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.db_connection import ping_mongo_db_server, setup_qdrant_collection
from service.csa.csa_setup import setup_agents, injest_data
from env_setup import set_runtime_env, app_settings
from app_state import state
from web.podcast import podcast
from web.csa import csa

set_runtime_env()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ping_mongo_db_server()
    state.client, state.embedding_model = setup_qdrant_collection(
        qdrant_url=app_settings.qdrant_url, qdrant_api_key=app_settings.qdrant_api_key
    )
    injest_data()
    state.processor_agent = setup_agents(app_settings.openai_api_key)
    print("Setup complete")

    try:
        yield
    except Exception as e:
        raise e
    finally:
        # cleanup
        if state.client:
            state.client.close()
        state.client = None
        state.embedding_model = None
        state.processor_agent = None


app = FastAPI(lifespan=lifespan)

app.include_router(podcast.router)
app.include_router(csa.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
