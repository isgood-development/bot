import asyncpg
import asyncio
from decouple import config
import random

import discord
from discord.ext import commands

DB_PW = config("DB_PW")
TOKEN = config("TOKEN")

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())

async def main():
    async with bot:
        bot.conn = await asyncpg.create_pool(database="testDB", user="postgres", password=DB_PW)
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    print("hey hey")

@bot.command(name='punish')
async def punish(ctx: commands.Context, member: discord.Member, *, reason: str):
    id = random.randint(0, 99999)
    await bot.conn.execute("INSERT INTO punishments (caseid, userid, punishment, reason) VALUES ($1, $2, $3, $4)", id, member.id, "terrorism", reason)
    await ctx.send("punishment added")

@bot.command()
async def punishments(ctx: commands.Context, member: discord.Member):
    data = await bot.conn.fetch("SELECT * FROM punishments WHERE userid = $1", member.id)
    e = []
    for case in data:
        if case['userid'] == member.id:
            e.append(f"ID: {case['caseid']} | Punishment: {case['punishment']} | Reason: {case['reason']}")

    if not e:
        return await ctx.send('no punishmentós')
    await ctx.send("\n".join(e))

asyncio.run(main())