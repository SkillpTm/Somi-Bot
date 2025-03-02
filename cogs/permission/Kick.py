import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Kick(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################
        
    @nextcord.slash_command(
        name = "kick",
        description = "kicks a member",
        default_member_permissions = nextcord.Permissions(kick_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def kick(
        self,
        interaction: nextcord.Interaction,
        *,
        member: nextcord.Member = nextcord.SlashOption(
            description = "Member to be kicked",
            required = True
        ),
        reason: str = nextcord.SlashOption(
            description = "Reason for the kick",
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command kicks a member with a reason."""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/ban",
            {"member": str(member.id), "reason": reason}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.followup.send(embed=EmbedFunctions().error("You can't ban yourself!"), ephemeral=True)
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.guild.owner:
            await interaction.followup.send(embed=EmbedFunctions().error("You can only kick a member, if your current top-role is above their current top-role!"), ephemeral=True)
            return
        
        try:
            if reason:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nFor the reason:\n`{reason}`")
            else:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nThere was no provided reason.")
        except:
            self.client.Loggers.action_warning(f"/kick send ~ User: {member.id} couldn't be notified, because their pms aren't open to the client")

        await interaction.guild.kick(user = member, reason = reason)

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully kicked {member.mention}."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(Kick(client))