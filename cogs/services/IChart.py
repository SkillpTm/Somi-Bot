import datetime
import zoneinfo

from bs4 import BeautifulSoup
import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.helpers import EmbedFunctions, Get
from lib.managers import Config, Commands
from lib.modules import SomiBot



class IChart(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["ichart"].name,
        Commands().data["ichart"].description,
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
    async def ichart(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """Gets the current iChart Top 10 Rankings"""

        await interaction.response.defer()
        response = requests.get("https://www.ichart.kr/rank", timeout=10)

        if response.status_code != 200:
            await interaction.send(embed=EmbedFunctions().get_error_message("iChart didn't respond correctly, try in a few minutes again!"))
            return None

        soup = BeautifulSoup(response.content, "html.parser")

        try:
            song_data, cover_image_url = self.get_rankings(soup)
        except Exception:
            await interaction.send(embed=EmbedFunctions().get_error_message("iChart didn't respond correctly, try in a few minutes again!"))
            return None

        output = ""
        for rank, song in song_data.items():
            if song["change"] is None:
                change = "(=)"
            elif song["change"]:
                change = f"(+{song['change_amount']})"
            else:
                change = f"(-{song['change_amount']})"

            output += f"`{rank}.` {change} **[{song['title']}]({song['url']})** by {song['artist']} - [{song['score']}]"
            output += f" `PAKs: {song['paks']}`\n\n" if song['paks'] else "\n\n"

        embed = EmbedFunctions().builder(
            color = Config().ICHART_COLOR,
            thumbnail = cover_image_url,
            author = "iChart Top 10",
            author_url = "https://www.ichart.kr/rank",
            author_icon = Config().ICHART_ICON,
            description = output,
            footer = "Score out of 220 points.",
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = self.get_last_half_past()
        )

        await interaction.send(embed=embed)


    @staticmethod
    def get_rankings(soup: BeautifulSoup) -> tuple[dict[int, dict[str, str | bool | None]], str]:
        """Uses the webscraped soup iChart to get the top 10 rankings data"""

        output: dict[int, dict[str, str | bool | None]] = {}
        cover_image_url = ""
        index = 0

        for container in soup.find_all("li", class_="group relative w-full"):
            if (index := index + 1) > 10:
                break

            if index == 1:
                cover_image_url = f"https://www.ichart.kr{container.find('img', class_='object-cover transition-opacity duration-300 opacity-0 rounded-[8px]')['src']}" # type: ignore

            output[index] = {}

            output[index]["title"] = Get.markdown_safe(container.select_one('[class^="body-contents-medium relative top-[2px] line-clamp-1 md:top-0 text-"]').text)
            output[index]["artist"] = Get.markdown_safe(container.find("p", class_="text-grayscale-500 body-caption-small relative top-[-2px] line-clamp-1 md:top-0").text)
            output[index]["url"] = f"https://www.ichart.kr{container.find('a', class_='flex w-full gap-3')['href']}" # type: ignore
            output[index]["score"] = container.select_one('[class^="title-feed flex min-w-[50px] flex-shrink-0 items-center justify-center text-right text-"]').text

            if (paks := container.find("div", class_="flex min-h-[12px] min-w-[32px] items-center justify-center rounded-[4px] p-1 text-center text-secondary-A-500 bg-secondary-A-000")):
                output[index]["paks"] = paks.text.replace("PAK ", "")
            else:
                output[index]["paks"] = None

            change = container.select_one('[class^="body-caption-meta flex items-center gap-1 relative h-"]')
            if change.find("img")["alt"] == "up": # type: ignore
                change_val = True
            elif change.find("img")["alt"] == "down": # type: ignore
                change_val = False
            else:
                change_val = None

            output[index]["change"] = change_val
            output[index]["change_amount"] = change.text if change_val is not None else None

        return output, cover_image_url


    @staticmethod
    def get_last_half_past() -> datetime.datetime:
        """ichart dynamically loads in the timestamps. The chart updates every 1hr, at :30 minutes past the hour. So we need to get the last :30 timestamp."""

        now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Seoul"))

        if now.minute < 30:
            rounded = now.replace(minute=30, second=0, microsecond=0) - datetime.timedelta(hours=1)
        else:
            rounded = now.replace(minute=30, second=0, microsecond=0)

        return rounded



def setup(client: SomiBot) -> None:
    client.add_cog(IChart(client))