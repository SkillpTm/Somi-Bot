import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import Misc



class OptionsButton(nextcord.ui.View):
    """A button to meant to be used to show all options"""

    def __init__(self, interaction: nextcord.Interaction[nextcord_C.Bot]) -> None:
        self.interaction = interaction
        self.value: bool | None = None
        super().__init__(timeout=300)


    @nextcord.ui.button(label="All Options", style=nextcord.ButtonStyle.gray)
    async def all_options(self, _button: nextcord.ui.Button[nextcord.ui.View], _interaction: nextcord.Interaction[nextcord_C.Bot]) -> None:
        """turns off the button and sets the value to true"""
        self.value = True
        self.stop()
        await Misc.deactivate_view_children(self)


    async def on_timeout(self) -> None:
        """overwrites the internal on_timeout to disable all buttons on timeout"""
        await Misc.deactivate_view_children(self)