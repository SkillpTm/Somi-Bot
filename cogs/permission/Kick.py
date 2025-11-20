import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Logger
from lib.modules import SomiBot



class Kick(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["kick"].name,
        Commands().data["kick"].description,
        default_member_permissions = nextcord.Permissions(kick_members=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def kick(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        member: nextcord.Member = nextcord.SlashOption(
            Commands().data["kick"].parameters["member"].name,
            Commands().data["kick"].parameters["member"].description,
            required = True
        ),
        reason: str = nextcord.SlashOption(
            Commands().data["kick"].parameters["reason"].name,
            Commands().data["kick"].parameters["reason"].description,
            required = False,
            min_length = 2,
            max_length = 1000
        )
    ) -> None:
        """This command kicks a member with a reason."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id == member.id:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can't ban yourself!"), ephemeral=True)
            return

        if interaction.user.top_role.position < member.top_role.position and interaction.user != interaction.guild.owner: # type: ignore
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You can only kick a member, if your current top-role is above their current top-role!"), ephemeral=True)
            return

        try:
            if reason:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nFor the reason:\n`{reason}`")
            else:
                await member.send(f"You have been __**kicked**__ from `{member.guild.name}`\nThere was no provided reason.")
        except nextcord.Forbidden:
            Logger().action_warning(f"/kick send ~ User: {member.id} couldn't be notified, because their pms aren't open to the client")

        await interaction.guild.kick(user = member, reason = reason)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Succesfully kicked {member.mention}."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(Kick(client))