###package#import###############################################################################

import nextcord
import os
import PIL

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class Color(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###color###########################################################

    @nextcord.slash_command(name = "color", description = "shows you what a color looks like")
    async def color(self,
                    interaction: nextcord.Interaction,
                    *,
                    hexcode: str = nextcord.SlashOption(description="input a color hexcode here", required=True, min_length=6, max_length=7)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /color {hexcode}")

        if not hexcode.startswith("#"):
            hexcode = f"#{hexcode}"

        try:
            hex_rgb = PIL.ImageColor.getcolor(hexcode, "RGB")
        except:
            await interaction.response.send_message("Please input a valid hex value for a color.", ephemeral=True)
            return

        for value in hex_rgb:
            if value < 0 or value > 256:
                await interaction.response.send_message("Please input a valid hex value for a color.", ephemeral=True)
                return

        color_image = PIL.Image.new('RGB', (300, 300), hex_rgb)

        color_image.save(f"./storage/temp/{hexcode}.png")

        await interaction.response.send_message(file = nextcord.File(f"./storage/temp/{hexcode}.png", f"{hexcode}.png"))

        os.remove(f"./storage/temp/{hexcode}.png")

        uses_update("command_uses", "color")



def setup(client):
    client.add_cog(Color(client))