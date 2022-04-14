# import discord
# from discord.ext import commands, tasks

# class Mod(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.mutes_task = self.check_mutes.start()
#         self.bans_task = self.check_bans.start()
    
#     @tasks.loop(minutes=2)
#     async def check_mutes(self):
#         mutes = await self.bot.mutes.get_all()
#         now = discord.utils.utcnow()
#         for item in mutes:
#             if now >= item["muteDuration"]:
#                 guild = await self.bot.fetch_guild(item["guildId"])
#                 member = await guild.fetch_member(item["_id"])
#                 data = await self.bot.muterole.find(guild.id)
#                 role = guild.get_role(data["muterole"])
#                 if role in member.roles:
#                     await member.remove_roles(role, reason = 'Temp-mute expiration')
                
#                 data = await self.bot.modlog.find(guild.id)
                
#                 if not data or "channel" not in data:
#                     return await self.bot.mutes.delete(member.id)
                
#                 try:
#                     channel = await self.bot.fetch_channel(data["channel"])
#                 except discord.NotFound:
#                     return await self.bot.mutes.delete(member.id)

#                 cases = int(data["cases"] + 1)
#                 await self.bot.modlog.upsert({"_id": guild.id, "cases": cases})

#                 e = discord.Embed(
#                     title=f'auto-unmute | case #{cases}',
#                     color=self.bot.blurple,
#                     description=f'{member} was unmuted as their temp-mute expired.'
#                 )
#                 e.set_thumbnail(url=member.avatar_url)
                
#                 await channel.send(embed=e)
#                 await self.bot.mutes.delete(member.id)
    
#     @tasks.loop(minutes=2)
#     async def check_bans(self):
#         bans = await self.bot.bans.get_all()
#         now = discord.utils.utcnow()
        
#         for item in bans:
#             if len(bans) != 0:
#                 if now >= item["banDuration"]:
#                     guild = self.bot.get_guild(item["guildId"])
#                     member = await self.bot.fetch_user(item["_id"])

#                     try:
#                         await guild.unban(member, reason = 'Temp-ban expiration')
#                     except discord.NotFound:
#                         return await self.bot.bans.delete(member.id)

#                     data = await self.bot.modlog.find(guild.id)
                    
#                     if not data or "channel" not in data:
#                         return
                    
#                     try:
#                         channel = guild.get_channel(data["channel"])
#                     except discord.NotFound:
#                         return await self.bot.bans.delete(member.id)

#                     cases = int(data["cases"] + 1)
#                     await self.bot.modlog.upsert({"_id": guild.id, "cases": cases})

#                     e = discord.Embed(
#                         title=f'auto-unban | case #{cases}',
#                         color=self.bot.blurple,
#                         description=f'{member} was unbanned as their temp-ban expired.'
#                     )
#                     e.set_thumbnail(url=member.avatar_url)
                    
#                     await channel.send(embed=e)
#                     await self.bot.bans.delete(member.id)

# async def setup(bot: commands.Bot):
#     await bot.add_cog(Mod(bot), guild=discord.Object(id=769281768821620746))