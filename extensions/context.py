import io
import discord
from discord.ext import commands
from discord import File

from .ext_views import DeleteButton

def send_as_file(content: str, *, filename: str=None):
    filename = filename if filename else "output"
    file = io.BytesIO()
    file.write(content)
    file.seek(0)

    return File(file, filename=f"{filename}.txt")
    
class ISgoodContext(commands.Context):
    """Extends the commands.Context class to add additional features."""
    async def send(self, content: str, **kwargs):
        if len(content) >= 2000:
            kwargs['file'] = send_as_file(content)
            return await super().reply("Response over 2000 characters:", **kwargs)

        return await super().reply(content, **kwargs)

class ISgoodInteraction(discord.InteractionResponse):
    async def send_message(content, **kwargs):
        if len(content) >= 2000:
            kwargs['file'] = send_as_file(content)
        
        button = DeleteButton()
        return await super().send_message(content, **kwargs)