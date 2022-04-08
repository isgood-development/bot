import asyncpg
import asyncio
from decouple import config

import discord
from discord import app_commands
from discord.ext import commands

extensions = [
    "cogs.mod"
]

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(".")(bot, message)

    return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

class ISgood(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        desc = "I am your worst nightmare."

        self.conn = None
        self.prefixes = {}
        self.startup_time = discord.utils.utcnow()

        super().__init__(
            command_prefix=get_prefix,
            description=desc,
            intents=intents,
            help_command=commands.MinimalHelpCommand(),
            case_insensitive=True,
            tree_cls=app_commands.CommandTree
        )

    def cache_prefixes(self):
        data = self.conn.fetch("SELECT * FROM prefixes")

        for item in data:
            bot.prefixes[item['guildid']] = item['prefix']

        for guild in bot.guilds:
            if not guild.id in bot.prefixes:
                bot.prefixes[guild.id] = "."


    async def setup_hook(self):
        self.conn = await asyncpg.create_pool(
            database="testDB",
            user="postgres",
            password=config("DB_PASSWORD")
        )
        print("database connected")

    async def on_ready(self):
        print(f"Logged in as '{self.user}'")
        self.cache_prefixes()


bot = ISgood()

@bot.command(name="synccmds")
async def synccmds(ctx):
    await bot.tree.sync(guild=discord.Object(id=769281768821620746))
    await ctx.send(":+1:")

async def main():
    async with bot:
        for cog in extensions:
            await bot.load_extension(cog)
        await bot.start(config("TOKEN"))

asyncio.run(main())