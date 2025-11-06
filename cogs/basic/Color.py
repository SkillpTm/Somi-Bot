import os
import re
import zlib

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot

WIDTH = 300
HEIGHT = 300



class Color(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="color", description="shows you what a color looks like")
    async def color(
        self,
        interaction: nextcord.Interaction,
        *,
        hexcode: str = nextcord.SlashOption(
            description = "input a color hexcode here",
            required = True,
            min_length = 6,
            max_length = 7
        )
    ) -> None:
        """This command converts a hexcode to an image of that color."""

        hexcode = hexcode.strip("#").lower()

        self.client.logger.action_log(Get.log_message(
            interaction,
            "/color",
            {"hexcode": hexcode}
        ))

        # check if the input is a valid hexcode
        if not re.match(r"^[0-9a-f]{6}$", hexcode):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please input a valid hex value for a color."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        self.generate_image(hexcode)

        await interaction.followup.send(file = nextcord.File(f"./debug/temp/{hexcode}.png", f"{hexcode}.png"))

        os.remove(f"./debug/temp/{hexcode}.png")

    ####################################################################################################

    @staticmethod
    def generate_image(hexcode: str) -> None:
        """Generates the image and stores it in ./debug/temp"""

        output_image = bytearray(b"\x89PNG\r\n\x1a\n")

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            return len(data).to_bytes(4, "big") + chunk_type + data + zlib.crc32(chunk_type + data).to_bytes(4, "big")

        output_image += chunk(
            b"IHDR",
            WIDTH.to_bytes(4, "big") +
            HEIGHT.to_bytes(4, "big") +
            b"\x08" +        # Bit depth
            b"\x02" +        # Color type: Truecolor RGB
            b"\x00" +        # Compression method
            b"\x00" +        # Filter method
            b"\x00"          # Interlace method
        )

        rgb_vals: list[int] = [int(hexcode[i:i+2], 16) for i in range(0, len(hexcode), 2)]
        raw_image_data = bytearray(
            b"".join(
                bytes([0]) + bytes(rgb_vals * WIDTH) for _ in range(HEIGHT)
            )
        )
        output_image += chunk(b"IDAT", zlib.compress(raw_image_data))
        output_image += chunk(b"IEND", b"")

        # we temporarily save the file to send it and then delete it again later
        with open(f"./debug/temp/{hexcode}.png", "wb") as file:
            file.write(output_image)



def setup(client: SomiBot) -> None:
    client.add_cog(Color(client))