# Import libraries
from pydantic_settings import BaseSettings, SettingsConfigDict

# Create class
class AccessKeysConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")

    OPENAI_API_KEY: str

#Instance
accesskeys_config = AccessKeysConfig()