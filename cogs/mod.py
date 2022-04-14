import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import checks


from utils.db import execute

class Mod(commands.Cog):
    """Moderation commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban-person")
    async def banuser(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        """Bans someone i think???"""
        execute(self.bot, "")
        await interaction.response.send_message(f"ok i will ban {member.name} for {reason}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Mod(bot), guild=discord.Object(id=769281768821620746))