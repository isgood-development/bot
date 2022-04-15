from typing import Union
import asyncpg
import asyncio
from decouple import config

import discord
from discord import app_commands
from discord.ext import commands

extensions = [
    "cogs.mod",
    "cogs.settings",
    # "cogs.tasks"
]

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(".")(bot, message)

    if message.guild.id not in bot.prefixes:
        return commands.when_mentioned_or(".")(bot, message)
    
    return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

class ISgood(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        self.conn = None
        self.prefixes = {}
        self.bans = []
        self.startup_time = discord.utils.utcnow()
        
        self.tick = '<:isgood_check:964533255439257630>' 
        self.cross = '<:isgood_cross:964533968068284456>' 

        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=commands.MinimalHelpCommand(),
            case_insensitive=True,
            tree_cls=app_commands.CommandTree
        )

    async def create_items(self):
        prefixes = await self.conn.fetch("SELECT * FROM prefixes")
        bans = await self.conn.fetch("SELECT * FROM botbans")

        for item in prefixes: # Cache custom guild prefixes
            self.prefixes[item['guild_id']] = item['prefix']

        for ban in bans: # Cache users that've been bot banned
            self.bans.append(ban)

    async def setup_hook(self):
        self.conn = await asyncpg.create_pool(
            database="testDB",
            user="postgres",
            password=config("DB_PASSWORD")
        )
        print("database connected")

    async def on_ready(self):
        print(f"Logged in as '{self.user}'")
        await self.create_items()

bot = ISgood()

@bot.tree.error
async def command_error(
        interaction: discord.Interaction, 
        command: Union[app_commands.Command, app_commands.ContextMenu],
        error: app_commands.AppCommandError
    ):
    if isinstance(error, app_commands.MissingPermissions):
        missing_perms = error.missing_permissions
        await interaction.response.send_message(f"{bot.cross} **You** are missing the following permission(s) to use this:\n`{', '.join(missing_perms)}`")

    if isinstance(error, app_commands.BotMissingPermissions):
        missing_perms = error.missing_permissions
        # TODO: add documentation for fixing this issue
        await interaction.response.send_message(f"{bot.cross} **The bot** is missing the following permission(s) to do this:\n`{', '.join(missing_perms)}`")

@bot.command(name="synccmds", aliases=['s'])
@commands.is_owner()
async def synccmds(ctx):
    await bot.tree.sync(guild=discord.Object(id=723237557009252404))
    await ctx.send(":+1:")

async def main():
    async with bot:
        for cog in extensions:
            await bot.load_extension(cog)
        await bot.start(config("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())