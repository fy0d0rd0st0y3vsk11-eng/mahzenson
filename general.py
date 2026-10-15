import discord
from discord import app_commands
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Mahzen bağlantısını kontrol eder.")
    async def ping(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"🏓 Pong! Gecikme: **{round(self.bot.latency * 1000)} ms**", ephemeral=True)

    @app_commands.command(name="sunucu", description="Sunucunun temel bilgilerini gösterir.")
    @app_commands.guild_only()
    async def sunucu(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("Bu komut yalnızca sunucuda kullanılabilir.", ephemeral=True)
            return
        embed = discord.Embed(title=f"🏰 {guild.name}", color=discord.Color.dark_green())
        embed.add_field(name="Üyeler", value=str(guild.member_count or "Bilinmiyor"))
        embed.add_field(name="Kuruluş", value=discord.utils.format_dt(guild.created_at, style="D"))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="yardim", description="Mahzen komutlarını listeler.")
    async def yardim(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="💚 Mahzen | Komutlar",
            description=("`/ping` — bağlantı kontrolü\n`/sunucu` — sunucu bilgileri\n`/yardim` — komut listesi\n`/ask` — OpenRouter AI\n`/anket` — iki seçenekli anket\n`/duyuru` — yönetici duyurusu\n`/temizle` — mesajları temizle"),
            color=discord.Color.dark_green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
