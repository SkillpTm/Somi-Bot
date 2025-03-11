import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import os
import PIL.Image
import PIL.ImageColor
import re

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Color(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "color", description = "shows you what a color looks like")
    @nextcord_AC.check(Checks.interaction_not_by_bot())
    async def color(
        self,
        interaction: nextcord.Interaction,
        *,
        hexcode: str = nextcord.SlashOption(
            description="input a color hexcode here",
            required=True,
            min_length=6,
            max_length=7
        )
    ) -> None:
        """This command converts a hexcode to an image of that color."""

        if not hexcode.startswith("#"):
            hexcode = f"#{hexcode}"

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/color",
            {"hexcode": hexcode}
        ))

        # check if the input is a valid hexcode
        if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', hexcode):
            await interaction.response.send_message(embed=EmbedFunctions().error("Please input a valid hex value for a color."), ephemeral=True)
            return
        
        await interaction.response.defer(with_message=True)

        # we temporarily save the file to send it and then delete it again later 
        color_image = PIL.Image.new('RGB', (300, 300), PIL.ImageColor.getcolor(hexcode, "RGB"))
        color_image.save(f"./debug/temp/{hexcode}.png")

        await interaction.followup.send(file = nextcord.File(f"./debug/temp/{hexcode}.png", f"{hexcode}.png"))

        os.remove(f"./debug/temp/{hexcode}.png")



def setup(client: SomiBot) -> None:
    client.add_cog(Color(client))