import nextcord

from lib.helpers import EmbedFunctions, Misc



class PageButtons(nextcord.ui.View):
    """Buttons that can flip through pages [start][<<<][current/max][>>>][end]"""

    def __init__(self, page: int, last_page: int, interaction: nextcord.Interaction) -> None:
        self.page: int = page
        self.last_page: int = last_page
        self.interaction: nextcord.Interaction = interaction
        self.value = None
        super().__init__(timeout=60)

    ####################################################################################################

    @nextcord.ui.button(label="start", style=nextcord.ButtonStyle.green)
    async def start(self, _button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        """returns to the first page"""

        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label="<<", style=nextcord.ButtonStyle.green)
    async def left(self, _button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        """goes back one page, without wrapping back to the end"""

        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = self.page-1 if self.page-1 >= 0 else 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label="/", style=nextcord.ButtonStyle.gray, disabled=True)
    async def page_button(self, _button: nextcord.ui.Button, _interaction: nextcord.Interaction) -> None:
        """does nothing, just displays the page numbers"""

    @nextcord.ui.button(label=">>", style=nextcord.ButtonStyle.red)
    async def right(self, _button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """goes forward one page, without wrapping back to the start"""

        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = self.page+1 if self.page+1 <= self.last_page else self.last_page
        self.value = True
        self.stop()

    @nextcord.ui.button(label="end", style=nextcord.ButtonStyle.red)
    async def end(self, _button: nextcord.ui.Button, interaction: nextcord.Interaction) -> None:
        """jumps to the last page"""

        if self.interaction.user.id != interaction.user.id:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You can only use buttons on your own commands."), ephemeral=True)
            return

        self.page = self.last_page
        self.value = True
        self.stop()

    ####################################################################################################

    async def update_buttons(self) -> None:
        """changes the page button numbers and checks, if the buttons should be disabled or nor"""

        await self._change_page_button()
        await self._check_page_for_button_deactivation()

    ####################################################################################################

    async def _change_page_button(self) -> None:
        """changes the number on the page button"""

        for child in self.children:
            if "/" in child.label:
                child.label = f"{self.page}/{self.last_page}"
        await self.interaction.edit_original_message(view=self)

    ####################################################################################################

    async def _check_page_for_button_deactivation(self) -> None:
        """disables buttons (all but the page button) in case they should be turned off"""

        # on the first page turn off the buttons that make you move back
        if self.page == 1:
            for child in self.children:
                if any(button_name in child.label for button_name in ["start", "<<"]):
                    child.disabled = True

        # on the last page turn off the buttons that make you move forward
        if self.page == self.last_page:
            for child in self.children:
                if any(button_name in child.label for button_name in [">>", "end"]):
                    child.disabled = True

        await self.interaction.edit_original_message(view=self)

    ####################################################################################################

    async def on_timeout(self) -> None:
        """overwrites the internal on_timeout to disable all buttons on timeout"""
        await Misc.deactivate_view_children(self)