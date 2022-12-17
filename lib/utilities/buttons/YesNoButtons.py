####################################################################################################

import nextcord

####################################################################################################

from lib.utilities.SomiBot import SomiBot



class YesNoButtons(nextcord.ui.View):
    
    def __init__(self,
                 *,
                 interaction: nextcord.Interaction = None,
                 response: nextcord.Message = None):
        super().__init__(timeout = 60)
        self.response = response
        self.interaction = interaction
        self.value: bool = None

    ####################################################################################################

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes(self,
                  button: nextcord.ui.Button,
                  interaction: nextcord.Interaction):
        self.value = True
        self.stop()
        await SomiBot.deactivate_view_children(self)

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no(self,
                 button: nextcord.ui.Button,
                 interaction: nextcord.Interaction):
        self.value = False
        self.stop()
        await SomiBot.deactivate_view_children(self)

    ####################################################################################################

    async def on_timeout(self):
        await SomiBot.deactivate_view_children(self)