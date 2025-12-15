from pydantic_settings import BaseSettings, SettingsConfigDict

class AccessKeysConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")

    OPENAI_API_KEY: str
    
accesskeys_config = AccessKeysConfig()