import os
import re
import zlib

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot



class Color(nextcord_C.Cog):

    WIDTH = 300
    HEIGHT = 300

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["color"].name,
        Commands().data["color"].description,
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def color(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        hexcode: str = nextcord.SlashOption(
            Commands().data["color"].parameters["hexcode"].name,
            Commands().data["color"].parameters["hexcode"].description,
            required = True,
            min_length = 6,
            max_length = 7
        )
    ) -> None:
        """This command converts a hexcode to an image of that color."""

        hexcode = hexcode.strip("#").lower()

        # check if the input is a valid hexcode
        if not re.match(r"^[0-9a-f]{6}$", hexcode):
            await interaction.send(embed=EmbedFunctions.get_error_message("Please input a valid hex value for a color."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        self.generate_image(hexcode)

        await interaction.send(file = nextcord.File(f"./debug/temp/{hexcode}.png", f"{hexcode}.png"))

        os.remove(f"./debug/temp/{hexcode}.png")


    @staticmethod
    def generate_image(hexcode: str) -> None:
        """Generates the image and stores it in ./debug/temp"""

        output_image = bytearray(b"\x89PNG\r\n\x1a\n")

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            return len(data).to_bytes(4, "big") + chunk_type + data + zlib.crc32(chunk_type + data).to_bytes(4, "big")

        output_image += chunk(
            b"IHDR",
            Color.WIDTH.to_bytes(4, "big") +
            Color.HEIGHT.to_bytes(4, "big") +
            b"\x08" +        # Bit depth
            b"\x02" +        # Color type: Truecolor RGB
            b"\x00" +        # Compression method
            b"\x00" +        # Filter method
            b"\x00"          # Interlace method
        )

        rgb_vals: list[int] = [int(hexcode[i:i+2], 16) for i in range(0, len(hexcode), 2)]
        raw_image_data = bytearray(
            b"".join(
                bytes([0]) + bytes(rgb_vals * Color.WIDTH) for _ in range(Color.HEIGHT)
            )
        )
        output_image += chunk(b"IDAT", zlib.compress(raw_image_data))
        output_image += chunk(b"IEND", b"")

        # we temporarily save the file to send it and then delete it again later
        with open(f"./debug/temp/{hexcode}.png", "wb") as file:
            file.write(output_image)



def setup(client: SomiBot) -> None:
    client.add_cog(Color(client))