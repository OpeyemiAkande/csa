from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    eleven_labs_api_key: str
    firecrawl_api_key: str
    qdrant_api_key: str
    qdrant_url: str
    doc_url: str
    mongo_uri: str
    mongo_db_name: str

    class Config:
        env_file = ".env"
