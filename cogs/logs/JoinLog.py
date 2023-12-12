####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import time

####################################################################################################

from lib.db_modules import AuditLogChannelDB, DefaultRoleDB, CommandUsesDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class JoinLog(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################
    
    @nextcord_C.Cog.listener()
    async def on_member_join(self,
                             member: nextcord.Member):
        """
        This function will:
        - Send a welcome message to Somicord
        - give the new member a default role, if set
        - create a join-log message, if teh guild has a join-log
        """

        self.client.Loggers.action_log(f"Guild: {member.guild.id} ~ User: {member.id} ~ join_log()")

        ####################################################################################################

        if member.guild.id == self.client.SOMICORD_ID:
            SOMICORD_WELCOME_CHANNEL = member.guild.get_channel(self.client.SOMICORD_WELCOME_CHANNEL_ID)
            welcome_embed = EmbedFunctions().builder(
                color = self.client.BOT_COLOR,
                description = f"Hey {member.mention}, welcome to `{member.guild.name}`!\nWhat you waiting for - start chatting.",
                image = self.client.SOMICORD_WELCOME_GIF
            )
            welcome_response = await SOMICORD_WELCOME_CHANNEL.send(embed=welcome_embed)
            await welcome_response.add_reaction(self.client.SOMI_WELCOME_EMOTE)

        ####################################################################################################

        default_role_id = DefaultRoleDB().get(member.guild)

        if default_role_id:
            await member.add_roles(member.guild.get_role(default_role_id))

        ####################################################################################################

        audit_log_id = AuditLogChannelDB().get(member.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = nextcord.Color.green(),
            thumbnail = member.display_avatar,
            title = f"New Member Joined: `{member.display_name}`",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "ID:",
                    member.id,
                    False
                ],

                [
                    "Name:",
                    member.mention,
                    True
                ],

                [
                    "Created at:",
                    f"<t:{int(time.mktime(member.created_at.timetuple()))}>",
                    True
                ]
            ]
        )

        audit_log_channel = member.guild.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)

        CommandUsesDB().uses_update("log_activations", "join log")



def setup(client: SomiBot):
    client.add_cog(JoinLog(client))