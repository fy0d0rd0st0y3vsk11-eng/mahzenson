import discord
from discord import app_commands
from discord.ext import commands

class AI(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ask", description="Mahzen AI'a soru sor (OpenRouter).")
    @app_commands.describe(soru="Yapay zekâya sormak istediğin soru")
    async def ask(self, interaction: discord.Interaction, soru: str) -> None:
        if len(soru) > 1500:
            await interaction.response.send_message("Soru en fazla 1500 karakter olabilir.", ephemeral=True)
            return
        await interaction.response.defer(thinking=True)
        try:
            answer = await self.bot.openrouter.ask(soru)
            await interaction.followup.send(answer, allowed_mentions=discord.AllowedMentions.none())
        except Exception:
            self.bot.logger.exception("OpenRouter isteği başarısız oldu")
            await interaction.followup.send("OpenRouter isteği başarısız oldu. API anahtarını, model adını ve servis durumunu kontrol et.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AI(bot))
