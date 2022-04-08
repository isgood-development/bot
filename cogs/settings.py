import discord
from discord import app_commands
from discord.ext import commands

class Settings(commands.Cog):
    """Server configuration commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="ban")
    async def banuser(self, interaction: discord.Interaction, member: discord.Member, *, reason: str):
        """Bans someone i think???"""
        await self.bot.conn.execute("INSERT INTO punishments (caseid, userid, punishment, reason) VALUES ($1, $2, $3, $4)", interaction.guild.id, member.id, "ban", reason)
        await interaction.response.send_message(f"ok i will ban {member.name} for {reason}")



async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot), guild=discord.Object(id=769281768821620746))