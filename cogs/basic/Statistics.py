import datetime
import math
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class Statistics(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["statistics"].alias,
        Commands().data["statistics"].description,
        name_localizations = {country_tag: Commands().data["statistics"].name for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def statistics(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        details: typing.Literal["Yes", ""] = nextcord.SlashOption(
            Commands().data["statistics"].parameters["details"].name,
            Commands().data["statistics"].parameters["details"].description,
            required = False,
            choices = ["Yes"],
            default = ""
        ),
        hidden: typing.Literal["No", ""] = nextcord.SlashOption(
            Commands().data["statistics"].parameters["hidden"].name,
            Commands().data["statistics"].parameters["hidden"].description,
            required = False,
            choices = ["No"],
            default = ""
        )
    ) -> None:
        """Shows statistics about a user on a server."""

        await interaction.response.defer(ephemeral=bool(not hidden), with_message=True)

        entry = await db.Statistic._.get_entry({db.Statistic.SERVER: interaction.guild.id, db.Statistic.USER: interaction.user.id})
        days_since_joined = math.ceil((datetime.datetime.now(datetime.timezone.utc) - interaction.user.joined_at).total_seconds() / 86400) # type: ignore
        footer, footer_time = self.client.joined_time_footer(interaction)

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = interaction.user.display_avatar.url,
            title = f"Server Statistics: `{interaction.user.display_name}`",
            footer = footer,
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = footer_time,
            fields = [
                EmbedField(
                    "Average:", # words/message, chars/message, messages/day
                    f"Words/Message: `{round(int(db.Statistic.WORDS.retrieve(entry) or 0) / int(db.Statistic.MESSAGES.retrieve(entry) or 0), 2)}`\n" +
                    f"Characters/Message: `{round(int(db.Statistic.CHARS.retrieve(entry) or 0) / int(db.Statistic.MESSAGES.retrieve(entry) or 0), 2)}`\n" +
                    f"Messages/Day: `{round(int(db.Statistic.MESSAGES.retrieve(entry) or 0) / days_since_joined, 2)}`\n",
                    False
                ),
                EmbedField(
                    "Messages:",
                    f"`{db.Statistic.MESSAGES.retrieve(entry)}`",
                    True
                ),
                EmbedField(
                    "Emotes:",
                    f"`{db.Statistic.EMOTES.retrieve(entry)}`",
                    True
                ),
                EmbedField(
                    "Reactions:",
                    f"`{db.Statistic.REACTIONS.retrieve(entry)}`",
                    True
                ),
                EmbedField(
                    f"{self.client.user.name} Commands:",
                    f"`{db.Statistic.COMMANDS.retrieve(entry)}`",
                    True
                ),
                EmbedField(
                    "Attachments:",
                    f"`{db.Statistic.ATTACHMENTS.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Characters:",
                    f"`{db.Statistic.CHARS.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Deletes:",
                    f"`{db.Statistic.DELETES.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Edits:",
                    f"`{db.Statistic.EDITS.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Links:",
                    f"`{db.Statistic.LINKS.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Replies:",
                    f"`{db.Statistic.REPLIES.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Stickers:",
                    f"`{db.Statistic.STICKERS.retrieve(entry)}`" if details else "",
                    True
                ),
                EmbedField(
                    "Words:",
                    f"`{db.Statistic.WORDS.retrieve(entry)}`" if details else "",
                    True
                )
            ]
        )

        await interaction.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Statistics(client))