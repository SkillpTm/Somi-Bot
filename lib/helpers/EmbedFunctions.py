import datetime

import nextcord

from lib.helpers.Get import Get
from lib.managers.Config import Config



class EmbedFunctions():
    """Helper class for embed related functions"""

    ####################################################################################################

    @staticmethod
    def get_critical_error_message(response: str) -> nextcord.Embed:
        """Makes an Embed for a critial error message"""

        embed = EmbedFunctions.builder(
            color = nextcord.Color.dark_red(),
            description = response
        )

        return embed

    ####################################################################################################

    @staticmethod
    def get_error_message(response: str) -> nextcord.Embed:
        """Makes an Embed for a error message"""

        embed = EmbedFunctions.builder(
            color = nextcord.Color.brand_red(),
            description = response
        )

        return embed

    ####################################################################################################

    @staticmethod
    def get_info_message(repsonse: str) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            description = repsonse
        )

        return embed

    ####################################################################################################

    @staticmethod
    def get_success_message(repsonse: str) -> nextcord.Embed:
        """Makes an Embed for a succes message"""

        embed = EmbedFunctions.builder(
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
            title = Get.rid_of_whitespace(f"{title[:256-3]}..." if len(title) > 256 else title), # 256 is Discord's title char limit
            url = title_url,
            description = Get.rid_of_whitespace(f"{description[:4096-3]}..." if len(description) > 4096 else description), # 4096 is Discord's description char limit
            color = color,
            timestamp = footer_timestamp if footer_timestamp else None
        )

        embed.set_author(name=Get.rid_of_whitespace(f"{author[:256-3]}..." if len(author) > 256 else author), url = author_url, icon_url = author_icon)  # 256 is Discord's author char limit
        embed.set_thumbnail(url=thumbnail)
        embed.set_image(url=image)
        embed.set_footer(text=Get.rid_of_whitespace(f"{footer[:2048-3]}..." if len(footer) > 2048 else footer), icon_url = footer_icon)  # 2048 is Discord's footer char limit

        for field in fields[:25]:  # 25 is Discord's field limit
            if not field[0]:
                break

            if not field[1]:
                break

            # fail save, should never have to happen
            if field[2] is None:
                field[2] = True

            embed.add_field(
                name = Get.rid_of_whitespace(f"{field[0][:256-3]}..." if len(field[0]) > 256 else field[0]),  # 256 is Discord's field name char limit
                value = Get.rid_of_whitespace(f"{field[1][:1024-3]}..." if len(field[1]) > 1024 else field[1]),  # 1024 is Discord's field value char limit
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
        if len(images) == 1 or (images and limit == 1):
            embed.set_image(url=images[0].url)

        # if there is no limit a and we have more than 1 attachment put them into a string
        if not limit and len(attachments_list) > 1:
            for attachment in attachments_list:
                file_urls += f"{attachment.url}\n"

        return embed, file_urls