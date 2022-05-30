import asyncio
import winerp 
from decouple import config, UndefinedValueError

import logging

import discord
from discord import app_commands
from discord.ext import commands

from extensions.context import ISgoodContext

logging.getLogger("winerp").setLevel(logging.DEBUG)

# extensions = [
#     # "cogs.mod",
#     # "cogs.settings",
#     "cogs.test",
#     # "cogs.ipc_routes"
# ]

def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(".")(bot, message)

    if message.guild.id not in bot.prefixes:
        return commands.when_mentioned_or(".")(bot, message)
    
    return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class ISgood(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            help_command=commands.MinimalHelpCommand(),
            case_insensitive=True,
            tree_cls=app_commands.CommandTree
        )
        self.conn = None
        self.loop 
        self.prefixes = {}
        self.bans = []
        self.startup_time = discord.utils.utcnow()

        self.ipc = winerp.Client("ig-bot", port=5464)
        
        self.tick = '<:isgood_check:964533255439257630>' 
        self.cross = '<:isgood_cross:964533968068284456>' 

    async def get_context(self, message, *, cls=ISgoodContext):
        return await super().get_context(message, cls=cls)

    # async def create_items(self):
    #     prefixes = await self.conn.fetch("SELECT * FROM prefixes")
    #     bans = await self.conn.fetch("SELECT * FROM botbans")

    #     for item in prefixes: # Cache custom guild prefixes
    #         self.prefixes[item['guild_id']] = item['prefix']

    #     for ban in bans: # Cache users that've been bot banned
    #         self.bans.append(ban)

    async def setup_hook(self):
        # self.conn = await asyncpg.create_pool(
        #     database="testDB",
        #     user="postgres",
        #     password=config("DB_PASSWORD")
        # )
        # print("database connected")
        pass

    async def on_ready(self):
        print(f"Logged in as '{self.user}'")
        # await self.create_items()

bot = ISgood()

@bot.ipc.route(name="get_guild_ids")
async def get_guild_ids():
    final = []
    for guild in bot.guilds:
        final.append(guild.id)

    return final

@bot.ipc.route(name="get_guild_data")
async def get_guild_data(guild_id):
    g = bot.get_guild(guild_id)
    
    if not g:
        return None
    
    # prefix = await bot.conn.fetch("SELECT * FROM prefixes WHERE guild_id = $1", guild_id)
    # modrole = await bot.conn.fetch("SELECT * FROM config WHERE guild_id = $1", guild_id)
    
    data = {
        "name": g.name,
        "icon_url": g.icon.url if g.icon else None,
        "created_at": g.created_at,
        "owner": g.owner.name,
        "channels": [str(channel) for channel in g.channels],
        "roles": [str(role) for role in g.roles],
        # "prefix": prefix if prefix else ".",
        # "modrole": modrole if modrole else None,
        "member_count": len(g.members),
        "member_count_no_bot": len([m for m in g.members if not m.bot])
    }
    
    return data 

# @bot.command(name="synccmds", aliases=['s'])
# @commands.is_owner()
# async def synccmds(ctx):
#     await bot.tree.sync(guild=discord.Object(id=723237557009252404))
#     await ctx.send(":+1:")

async def main():
    async with bot:
        # for cog in extensions:
        #     await bot.load_extension(cog)

        bot.loop.create_task(bot.ipc.start())
        
        try:
            await bot.start(config("TOKEN"))
        except UndefinedValueError:
            raise ValueError("You haven't provided a token in the '.env' file.")

if __name__ == "__main__":
    asyncio.run(main())