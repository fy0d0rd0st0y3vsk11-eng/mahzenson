import asyncio
import logging
import os

import discord
from discord.ext import commands

from app.ai import OpenRouterClient
from app.config import Settings
from app.database import Database

def configure_logging() -> logging.Logger:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper(), format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    return logging.getLogger("mahzen")

class MahzenBot(commands.Bot):
    def __init__(self, settings: Settings, logger: logging.Logger):
        super().__init__(command_prefix="!", intents=discord.Intents.default(), help_command=None, allowed_mentions=discord.AllowedMentions.none())
        self.settings = settings
        self.logger = logger
        self.database = Database(settings.database_path)
        self.openrouter = OpenRouterClient(settings.openrouter_api_key, settings.openrouter_model, settings.openrouter_site_url, settings.openrouter_app_name)

    async def setup_hook(self) -> None:
        for extension in ("app.cogs.general", "app.cogs.ai", "app.cogs.community"):
            await self.load_extension(extension)
            self.logger.info("Eklenti yüklendi: %s", extension)
        synced = await self.tree.sync()
        self.logger.info("%s slash komutu Discord ile eşitlendi.", len(synced))

    async def on_ready(self) -> None:
        self.logger.info("Giriş yapıldı: %s (ID: %s)", self.user, self.user.id if self.user else "?")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Mahzen'i | /yardim"))

async def main() -> None:
    logger = configure_logging()
    settings = Settings.load()
    settings.validate()
    bot = MahzenBot(settings, logger)
    try:
        await bot.start(settings.discord_token)
    finally:
        await bot.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception:
        logging.getLogger("mahzen").exception("Bot başlatılamadı.")
        raise
