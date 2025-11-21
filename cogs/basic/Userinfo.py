import time

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot



class Userinfo(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["userinfo"].alias,
        Commands().data["userinfo"].description,
        name_localizations = {country_tag: Commands().data["userinfo"].name for country_tag in nextcord.Locale},
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def userinfo(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["userinfo"].parameters["user"].name,
            Commands().data["userinfo"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command gives you infomration about a user"""

        await interaction.response.defer(with_message=True)

        user = user or interaction.user

        # empty server data, if left empty the coresponding fields will not be dispalyed
        booster, joined_time, status, top_role = "", "", "", ""

        # if the command was made in a guild also add data regarding the guild
        if interaction.guild and (member := interaction.guild.get_member(user.id)):
            status = str(member.status)
            top_role = member.top_role.mention
            booster = "Yes" if member.premium_since else "No"
            joined_time = f"<t:{int(time.mktime(member.joined_at.timetuple()))}>"

        embed = EmbedFunctions().builder(
            color = user.color,
            thumbnail = user.display_avatar.url,
            title = f"User Information: `{user.display_name}`",
            fields = [
                EmbedField(
                    "ID:",
                    str(user.id),
                    False
                ),
                EmbedField(
                    "Username:",
                    user.name,
                    True
                ),
                EmbedField(
                    "Display Name:",
                    user.display_name,
                    True
                ),
                EmbedField(
                    "Status:",
                    status,
                    True
                ),
                EmbedField(
                    "Top role:",
                    top_role,
                    True
                ),
                EmbedField(
                    "Booster:",
                    booster,
                    True
                ),
                EmbedField(
                    "Joined Discord:",
                    f"<t:{int(time.mktime(user.created_at.timetuple()))}>",
                    True
                ),
                EmbedField(
                    "Joined Server:",
                    joined_time,
                    True
                ),
                EmbedField(
                    "Public Flags:",
                    ", ".join(flag.name for flag in user.public_flags.all()),
                    False
                )
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Userinfo(client))