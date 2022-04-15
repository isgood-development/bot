import discord

class ISgoodEmbed(discord.Embed):
    """An extension if discord.Embed to add features that
    make the response a bit more 'consistent' with other responses"""
    def __init__(self, description=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = description if description else None
        self.color = 0x5865F2