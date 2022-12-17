####################################################################################################

import datetime
import nextcord
import pytz

####################################################################################################



class EmbedFunctions():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    def critical_error(self,
                       response: str) -> nextcord.Embed:
        """Makes an Embed for a critial error message"""

        embed = self.builder(
            color = nextcord.Color.dark_red(),
            description = response
        )

        return embed

    ####################################################################################################

    def info_message(self,
                     repsonse: str,
                     client) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = self.builder(
            color = client.BOT_COLOR,
            description = repsonse
        )

        return embed

    ####################################################################################################

    def error(self,
              response: str) -> nextcord.Embed:
        """Makes an Embed for a error message"""

        embed = self.builder(
            color = nextcord.Color.brand_red(),
            description = response
        )

        return embed

    ####################################################################################################

    def success(self,
                repsonse: str) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = self.builder(
            color = nextcord.Color.brand_green(),
            description = repsonse
        )

        return embed

    ####################################################################################################

    @staticmethod
    def get_attachments(attachments_list: list[nextcord.Attachment],
                        embed: nextcord.Embed,
                        limit: int = None) -> tuple[nextcord.Embed, str]:
        """This function adds an image to the embed, if it's onyl 1 image, otherwise it writes the file urls into a string. On 0 embeds nothing changes"""

        file_urls: str = ""

        if len(attachments_list) == 1 or len(attachments_list) > 0 and limit == 1:
            if "image" in attachments_list[0].content_type:
                embed.set_image(url=attachments_list[0].url)
            else:
                file_urls += attachments_list[0].url

        elif len(attachments_list) > 1:
            for attachment in attachments_list:
                file_urls += f"{attachment.url}\n"

        return embed, file_urls
    
    ####################################################################################################

    @staticmethod
    def builder(color: int | nextcord.Color = None,
                thumbnail: str = "",
                image: str = "",

                author: str = "",
                author_url: str = "",
                author_icon: str = "",

                title: str = "",
                title_url: str = "",

                description: str = "",

                footer: str = "",
                footer_icon: str = "",

                fields: list[list[tuple[str, str, bool]]] = []) -> nextcord.Embed:
        """This function builds an embed and adds a default timestamp, if specified"""

        embed = nextcord.Embed(title = title[:256],
                               url = title_url,
                               description = description[:4096],
                               color = color)

        embed.set_author(name = author[:256], url = author_url, icon_url = author_icon)
        embed.set_thumbnail(url = thumbnail)
        embed.set_image(url = image)

        if footer == "DEFAULT_KST_FOOTER":
            from lib.utilities.SomiBot import SomiBot
            
            embed.set_footer(text = datetime.datetime.now(pytz.timezone('Asia/Seoul')).strftime("%Y/%m/%d %H:%M:%S %Z"), icon_url = SomiBot.CLOCK_ICON)
        else:
            embed.set_footer(text = footer[:2048], icon_url = footer_icon)

        for field in fields[:25]:
            if field[0] == "" or field[0] == None:
                break

            if field[1] == "" or field[1] == None:
                break

            if field[2] == None:
                field[2] = True
            
            embed.add_field(name = f"{field[0]}"[:256], value = f"{field[1]}"[:1024], inline = field[2])

        return embed