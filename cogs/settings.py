from code import interact
import discord
from discord import app_commands
from discord.app_commands import checks
from discord.ext import commands

from utils.db import execute, fetch

class Settings(commands.Cog):
    """Server configuration commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    group = app_commands.Group(name="config", description="A group of commands used for configuring bot settings.")

    @group.command(name="modrole")
    @app_commands.describe(role="Optional role to set.")
    @checks.has_permissions(manage_guild=True)
    async def modrole(self, inter: discord.Interaction, role: discord.Role=None):
        """Assigns the modrole to a role in your server."""
        if role:
            data = execute(self.bot, "INSERT INTO config (guild_id, modrole) VALUES ($1, $2)", inter.guild_id, role.id)
            print(data)
            # await inter.response.send_message(f"The modrole has been binded to the role {role.mention}", ephemeral=True)
        else:
            role = fetch(self.bot, "SELECT * FROM config WHERE guild_id = $1", inter.guild_id)
            print(role)
        


async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot), guild=discord.Object(id=769281768821620746))