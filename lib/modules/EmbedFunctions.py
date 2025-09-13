import datetime
import nextcord

from lib.modules.Get import Get



class EmbedFunctions():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    def get_critical_error_message(self, response: str) -> nextcord.Embed:
        """Makes an Embed for a critial error message"""

        embed = self.builder(
            color = nextcord.Color.dark_red(),
            description = response
        )

        return embed

    ####################################################################################################

    def get_error_message(self, response: str) -> nextcord.Embed:
        """Makes an Embed for a error message"""

        embed = self.builder(
            color = nextcord.Color.brand_red(),
            description = response
        )

        return embed

    ####################################################################################################

    def get_info_message(self, repsonse: str, client) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = self.builder(
            color = client.BOT_COLOR,
            description = repsonse
        )

        return embed

    ####################################################################################################

    def get_success_message(self, repsonse: str) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = self.builder(
            color = nextcord.Color.green(),
            description = repsonse
        )

        return embed

    ####################################################################################################

    @staticmethod
    def builder(
        color: int | nextcord.Color | None = None,
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
        footer_timestamp: datetime.datetime | None = None,

        fields: list[list[tuple[str, str, bool]]] = []
    ) -> nextcord.Embed:
        """This function builds an embed"""

        embed = nextcord.Embed(
            title = Get.rid_of_whitespace(title[:256]), # 256 is Discord's title char limit
            url = title_url,
            description = Get.rid_of_whitespace(description[:4096]), # 4096 is Discord's description char limit
            color = color,
        )

        embed.set_author(name = Get.rid_of_whitespace(author[:256]), url = author_url, icon_url = author_icon)  # 256 is Discord's author char limit
        embed.set_thumbnail(url = thumbnail)
        embed.set_image(url = image)
        embed.set_footer(text = Get.rid_of_whitespace(footer[:2048]), icon_url = footer_icon)  # 2048 is Discord's footer char limit

        if footer_timestamp:
            embed.timestamp = footer_timestamp

            if not footer_icon:
                from lib.utilities.SomiBot import SomiBot
                embed.set_footer(text = Get.rid_of_whitespace(footer[:2048]), icon_url = SomiBot.CLOCK_ICON)

        for field in fields[:25]:  # 25 is Discord's field limit
            if not field[0]:
                break

            if not field[1]:
                break

            # fail save, should never have to happen
            if field[2] == None:
                field[2] = True
            
            embed.add_field(
                name = Get.rid_of_whitespace(f"{field[0]}"[:256]),  # 256 is Discord's field name char limit
                value = Get.rid_of_whitespace(f"{field[1]}"[:1024]),  # 1024 is Discord's field value char limit
                inline = field[2]
            )

        return embed

    ####################################################################################################

    @staticmethod
    def get_or_add_attachments(
        attachments_list: list[nextcord.Attachment],
        embed: nextcord.Embed,
        limit: int = 0
    ) -> tuple[nextcord.Embed, str]:
        """This function adds an image to the embed, if it's only 1 image or the limit is 1, otherwise it writes the file urls into a string. On 0 images the embed doesn't change"""

        file_urls: str = ""
        images: list[nextcord.Attachment] = []

        for attachment in attachments_list:
            if "image" in attachments_list[0].content_type:
                images.append(attachment)

        # if we only have 1 image or a limit of 1 embed the first image
        if len(images) == 1 or (len(images) and limit == 1):
            embed.set_image(url=images[0].url)

        # if there is no limit a and we have more than 1 attachment put them into a STRING
        if not limit and len(attachments_list) > 1:
            for attachment in attachments_list:
                file_urls += f"{attachment.url}\n"

        return embed, file_urls