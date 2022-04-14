import discord

class DeleteButton(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout=20
        self.delete = False
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.author.id != self.interaction_context.id:
            return True
        return False
    
    @discord.ui.button(style=discord.ButtonStyle.red, label="\U0001f5d1")
    async def btnDelete(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.interaction_context.delete_original_message()
        self.delete = True
        self.stop()
