import io
from discord.ext import commands
from discord import File

def send_as_file(content: str, *, filename: str=None):
    filename = filename if filename else "output"
    file = io.BytesIO()
    file.write(content)
    file.see(0)

    return File(file, filename=f"{filename}.txt")

class ISgoodContext(commands.Context):
    """Extends the commands.Context class to add additional features."""
    async def send(self, content: str, **kwargs):
        if len(content) >= 2000:
            kwargs['file'] = send_as_file(content)
            return super().reply(content, **kwargs)

        return super().reply(content, **kwargs)