import nextcord

from lib.modules.EmbedFunctions import EmbedFunctions
from lib.utilities.SomiBot import SomiBot



class PageButtons(nextcord.ui.View):

    def __init__(self, page, last_page, interaction):
        self.value = None
        self.page: int = page
        self.last_page: int = last_page
        self.interaction: nextcord.Interaction = interaction
        super().__init__(timeout = 60)

    ####################################################################################################

    @nextcord.ui.button(label = "start", style=nextcord.ButtonStyle.green)
    async def start(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().error("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "<<", style=nextcord.ButtonStyle.green)
    async def left(self,
                   button: nextcord.ui.Button,
                   interaction: nextcord.Interaction):
        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().error("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page -= 1
        if self.page == 0:
            self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "/", style=nextcord.ButtonStyle.gray, disabled=True)
    async def page_button(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        pass

    @nextcord.ui.button(label = ">>", style=nextcord.ButtonStyle.red)
    async def right(self,
                    button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().error("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page += 1
        if self.page > self.last_page:
            self.page = self.last_page
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "end", style=nextcord.ButtonStyle.red)
    async def end(self,
                  button: nextcord.ui.Button,
                  interaction: nextcord.Interaction):
        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().error("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = self.last_page
        self.value = True
        self.stop()

    ####################################################################################################

    async def update_buttons(self):
        await self.change_page_button()
        await self.check_page_for_button_deactivation()

    ####################################################################################################

    async def change_page_button(self):
        for child in self.children:
            if "/" in child.label:
                child.label = f"{self.page}/{self.last_page}"
        await self.interaction.edit_original_message(view=self)

    ####################################################################################################

    async def check_page_for_button_deactivation(self):
        if self.page == 1:
            for child in self.children:
                if any(button_name in child.label for button_name in ["start", "<<"]):
                    child.disabled = True

        if self.page == self.last_page:
            for child in self.children:
                if any(button_name in child.label for button_name in [">>", "end"]):
                    child.disabled = True

        await self.interaction.edit_original_message(view=self)

    ####################################################################################################

    async def on_timeout(self):
        await SomiBot.deactivate_view_children(self)