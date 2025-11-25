import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from cogs.basic.ParentCommand import ParentCommand
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config
from lib.modules import SomiBot, YesNoButtons



class Shutdown(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.sudo.subcommand(Commands().data["sudo shutdown"].name, Commands().data["sudo shutdown"].description)
    @nextcord_AC.check(Get.interaction_by_owner()) # type: ignore
    async def shutdown(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command let's you shutdown the bot, it can only be executed from a moderator on Somicord."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to shutdown the bot?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("The bot has not been shutdown"))
            return

        await interaction.send(embed=EmbedFunctions().get_success_message("The bot is being shutdown..."))


        embed = EmbedFunctions().builder(
            color = nextcord.Color.orange(),
            author = "Dev Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                EmbedField(
                    f"/{Commands().data["sudo shutdown"].full_name}:",
                    f"{interaction.user.mention} shutdown the bot",
                    False
                )
            ]
        )

        await self.client.get_channel(Config().SUPPORT_SERVER_LOGS_ID).send(embed=embed) # type: ignore
        await self.client.close()



def setup(client: SomiBot) -> None:
    client.add_cog(Shutdown(client))