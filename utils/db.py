from discord.ext import commands

async def execute(bot: commands.Bot, query: str, *values):
    return await bot.conn.execute(query, *values)

async def fetch(bot: commands.Bot, query: str, *values):
    return await bot.conn.fetch(query, *values)