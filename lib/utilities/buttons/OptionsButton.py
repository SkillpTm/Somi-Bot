import nextcord

from lib.modules import Misc



class OptionsButton(nextcord.ui.View):
    
    def __init__(self, interaction: nextcord.Interaction = None) -> None:
        super().__init__(timeout = 300)
        self.interaction = interaction
        self.value: bool = None

    ####################################################################################################

    @nextcord.ui.button(label = "All Options", style=nextcord.ButtonStyle.gray)
    async def all_options(self, button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        self.value = True
        self.stop()
        await Misc.deactivate_view_children(self)

    ####################################################################################################

    async def on_timeout(self) -> None:
        """overwrites the internal on_timeout to disable all buttons on timeout"""
        await Misc.deactivate_view_children(self)