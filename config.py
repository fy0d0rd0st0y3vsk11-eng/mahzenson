from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    discord_token: str
    openrouter_api_key: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str
    database_path: str

    @classmethod
    def load(cls) -> "Settings":
        return cls(
            discord_token=os.getenv("DISCORD_TOKEN", "").strip(),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", "").strip(),
            openrouter_model=os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini").strip(),
            openrouter_site_url=os.getenv("OPENROUTER_SITE_URL", "").strip(),
            openrouter_app_name=os.getenv("OPENROUTER_APP_NAME", "Mahzen Bot").strip(),
            database_path=os.getenv("DATABASE_PATH", "data/mahzen.sqlite3").strip(),
        )

    def validate(self) -> None:
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN eksik. Hosting panelinin Environment Variables alanına ekle.")
        if not self.openrouter_model:
            raise ValueError("OPENROUTER_MODEL boş olamaz.")
