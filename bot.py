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

        print(prefixes)
        print(bans)

        for item in prefixes: # Cache custom guild prefixes
            self.prefixes[item['guild_id']] = item['prefix']

        for guild in bot.guilds: # Cache prefixes that haven't been customized in the rest of the guilds
            if not guild.id in bot.prefixes:
                self.prefixes[guild.id] = "."

        for ban in bans: # Cache users that've been bot banned
            self.bans.append(ban)
        
        print(self.bans)
        print(self.prefixes)

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

@bot.command(name="synccmds")
async def synccmds(ctx):
    await bot.tree.sync(guild=discord.Object(id=769281768821620746))
    await ctx.send(":+1:")

async def main():
    async with bot:
        for cog in extensions:
            await bot.load_extension(cog)
        await bot.start(config("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())