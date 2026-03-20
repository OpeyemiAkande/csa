import os
from settings import Settings

app_settings = Settings()  # type: ignore


def set_runtime_env():
    """
    Ensures API keys are available to tools that expect them as OS env vars.
    """
    os.environ["OPENAI_API_KEY"] = app_settings.openai_api_key
    os.environ["ELEVEN_LABS_API_KEY"] = app_settings.eleven_labs_api_key
    os.environ["FIRECRAWL_API_KEY"] = app_settings.firecrawl_api_key
