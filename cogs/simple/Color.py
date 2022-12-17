####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import os
import PIL.Image
import PIL.ImageColor
import re

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Color(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "color", description = "shows you what a color looks like")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def color(self,
                    interaction: nextcord.Interaction,
                    *,
                    hexcode: str = nextcord.SlashOption(description="input a color hexcode here", required=True, min_length=6, max_length=7)):
        """This command converts a hexcode to an image of that color."""

        if not hexcode.startswith("#"):
            hexcode = f"#{hexcode}"

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /color {hexcode}")

        await interaction.response.defer(with_message=True)

        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', hexcode):
            hex_rgb = PIL.ImageColor.getcolor(hexcode, "RGB")
        else:
            await interaction.followup.send(embed=EmbedFunctions().error("Please input a valid hex value for a color."))
            return

        color_image = PIL.Image.new('RGB', (300, 300), hex_rgb)

        color_image.save(f"./storage/temp/{hexcode}.png")

        await interaction.followup.send(file = nextcord.File(f"./storage/temp/{hexcode}.png", f"{hexcode}.png"))

        os.remove(f"./storage/temp/{hexcode}.png")



def setup(client: SomiBot):
    client.add_cog(Color(client))