import nextcord

from lib.modules import EmbedFunctions, Misc



class YesNoButtons(nextcord.ui.View):
    
    def __init__(self, *, interaction: nextcord.Interaction = None, response: nextcord.Message = None) -> None:
        super().__init__(timeout = 60)
        self.response = response
        self.interaction = interaction
        self.value: bool = None

    ####################################################################################################

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        if self.interaction:
            original_user = self.interaction.user
        elif self.response:
            original_user = self.response.author

        if original_user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.value = True
        self.stop()
        await Misc.deactivate_view_children(self)

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        if self.interaction:
            original_user = self.interaction.user
        elif self.response:
            original_user = self.response.author

        if original_user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.value = False
        self.stop()
        await Misc.deactivate_view_children(self)

    ####################################################################################################

    async def on_timeout(self) -> None:
        """overwrites the internal on_timeout to disable all buttons on timeout"""
        await Misc.deactivate_view_children(self)