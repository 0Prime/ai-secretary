import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    obsidian_vault_path: Path = Field(
        default=Path(r"D:\_Documents\Obsidian"),
        description="Path to Obsidian vault"
    )
    secretary_data_path: Path = Field(
        default=Path.home() / ".secretary",
        description="Path to Secretary data directory"
    )
    
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    siliconflow_api_key: str | None = Field(default=None, alias="SILICONFLOW_API_KEY")
    zhipu_api_key: str | None = Field(default=None, alias="ZHIPU_API_KEY")
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    
    default_ai_provider: str = Field(default="ollama")
    ollama_model: str = Field(default="llama3.2:1b")
    
    proxy_url: str | None = Field(default=None, alias="PROXY_URL")

    @model_validator(mode="after")
    def setup_paths(self):
        self.secretary_data_path.mkdir(parents=True, exist_ok=True)
        self._load_proxy_from_obsidian()
        self._apply_proxy_env()
        return self
    
    def _load_proxy_from_obsidian(self):
        if self.proxy_url:
            return
        
        proxy_file = self.obsidian_vault_path / "Work" / "Idea proxy settings.md"
        if proxy_file.exists():
            content = proxy_file.read_text().strip()
            if content:
                parts = content.split()
                if len(parts) >= 2:
                    host = parts[0]
                    port = parts[1]
                    self.proxy_url = f"http://{host}:{port}"
    
    def _apply_proxy_env(self):
        if self.proxy_url:
            os.environ["HTTP_PROXY"] = self.proxy_url
            os.environ["HTTPS_PROXY"] = self.proxy_url
            os.environ["http_proxy"] = self.proxy_url
            os.environ["https_proxy"] = self.proxy_url

    @property
    def secretary_db_path(self) -> Path:
        return self.secretary_data_path / "secretary.db"
    
    @property
    def secretary_vector_path(self) -> Path:
        return self.secretary_data_path / "chroma"


settings = Settings()
