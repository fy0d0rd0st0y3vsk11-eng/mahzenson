import discord
from discord import app_commands
from discord.ext import commands

class Community(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="anket", description="İki seçenekli tepki anketi oluşturur.")
    @app_commands.describe(soru="Anket sorusu", secenek1="Birinci seçenek", secenek2="İkinci seçenek")
    @app_commands.guild_only()
    async def anket(self, interaction: discord.Interaction, soru: str, secenek1: str, secenek2: str) -> None:
        if len(soru) > 250 or len(secenek1) > 80 or len(secenek2) > 80:
            await interaction.response.send_message("Soru en fazla 250, seçenekler 80 karakter olabilir.", ephemeral=True)
            return
        embed = discord.Embed(title="📊 Mahzen Anketi", description=f"**{discord.utils.escape_markdown(soru)}**", color=discord.Color.dark_green())
        embed.add_field(name="🇦", value=discord.utils.escape_markdown(secenek1), inline=True)
        embed.add_field(name="🇧", value=discord.utils.escape_markdown(secenek2), inline=True)
        embed.set_footer(text=f"Oluşturan: {interaction.user}")
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        for emoji in ("🇦", "🇧"):
            try:
                await message.add_reaction(emoji)
            except discord.HTTPException:
                self.bot.logger.warning("Anket tepkisi eklenemedi: %s", emoji)

    @app_commands.command(name="duyuru", description="Sunucuya duyuru gönderir.")
    @app_commands.describe(mesaj="Duyuru metni")
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    async def duyuru(self, interaction: discord.Interaction, mesaj: str) -> None:
        if not interaction.permissions.administrator:
            await interaction.response.send_message("Bu komut için Yönetici izni gerekiyor.", ephemeral=True)
            return
        if len(mesaj) > 1800:
            await interaction.response.send_message("Duyuru en fazla 1800 karakter olabilir.", ephemeral=True)
            return
        channel = interaction.channel
        if channel is None or not hasattr(channel, "send"):
            await interaction.response.send_message("Bu kanala mesaj gönderilemiyor.", ephemeral=True)
            return
        embed = discord.Embed(description=mesaj, color=discord.Color.dark_green())
        embed.set_author(name=f"📢 {interaction.guild.name if interaction.guild else 'Mahzen'} Duyuru")
        await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())
        await interaction.response.send_message("Duyuru gönderildi. 💚", ephemeral=True)

    @app_commands.command(name="temizle", description="Son mesajları temizler.")
    @app_commands.describe(adet="Silinecek mesaj sayısı (1-50)")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def temizle(self, interaction: discord.Interaction, adet: app_commands.Range[int, 1, 50]) -> None:
        if not interaction.permissions.manage_messages:
            await interaction.response.send_message("Bu komut için Mesajları Yönet izni gerekiyor.", ephemeral=True)
            return
        channel = interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.Thread)):
            await interaction.response.send_message("Bu kanalda mesaj temizleyemiyorum.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            deleted = await channel.purge(limit=int(adet))
            await interaction.followup.send(f"🧹 {len(deleted)} mesaj temizlendi.", ephemeral=True)
        except discord.Forbidden:
            await interaction.followup.send("Botun Mesajları Yönet izni yok.", ephemeral=True)
        except discord.HTTPException:
            await interaction.followup.send("Discord mesajları temizleyemedi. Daha sonra tekrar dene.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Community(bot))
