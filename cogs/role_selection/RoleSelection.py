####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C

####################################################################################################

from lib.db_modules import CommandUsesDB
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot



class Roles(nextcord.ui.View):
    
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client: SomiBot = client

    ####################################################################################################

    async def handle_click(self,
                           button: nextcord.ui.Button,
                           interaction: nextcord.Interaction):
        """This function adds/removes the given role to/from a user, depending on, if they already have the given role"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        role: nextcord.Role = interaction.guild.get_role(int(button.custom_id))

        if role in interaction.user.roles:
            self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ rolelist() remove {role.id}")

            await interaction.user.remove_roles(role)
            await interaction.followup.send(embed=EmbedFunctions().error(f"The role: {role.mention} has been removed form your role list"), ephemeral=True)

            CommandUsesDB().uses_update("role_selections", f"remove {role.name}")
        else:
            self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ rolelist() add {role.id}")

            await interaction.user.add_roles(role)
            await interaction.followup.send(embed=EmbedFunctions().success(f"The role: {role.mention} has been added to your role list"), ephemeral=True)

            CommandUsesDB().uses_update("role_selections", f"add {role.name}")

    ####################################################################################################

    @nextcord.ui.button(label = "UPDATES", style = nextcord.ButtonStyle.blurple, custom_id = f"{SomiBot.Lists.SOMICORD_UPDATE_ROLES_IDS['UPDATES_ID']}")
    async def UPDATES(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "LIVE", style = nextcord.ButtonStyle.blurple, custom_id = f"{SomiBot.Lists.SOMICORD_UPDATE_ROLES_IDS['LIVE_ID']}")
    async def LIVE(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "SNS", style = nextcord.ButtonStyle.blurple, custom_id = f"{SomiBot.Lists.SOMICORD_UPDATE_ROLES_IDS['SNS_ID']}")
    async def SNS(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "REDDIT", style = nextcord.ButtonStyle.blurple, custom_id = f"{SomiBot.Lists.SOMICORD_UPDATE_ROLES_IDS['REDDIT_ID']}")
    async def REDDIT(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "ROLES", style=nextcord.ButtonStyle.gray, custom_id="SOMICORD.ROLES")
    async def ROLES(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        """This function outputs anyone user's roles, upon button press"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ rolelist() ROLES")

        await interaction.response.defer(ephemeral=True, with_message=True)

        rolelist = [role.mention for role in interaction.user.roles if role != interaction.guild.default_role]
        output = ""

        for i in range(len(rolelist)):
            output += f"{i + 1}. {rolelist[i]}\n"

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"Rolelist for {interaction.user}",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Roles:",
                    output[:1000],
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)

        CommandUsesDB().uses_update("role_selections", "clicked ROLES")



class RoleSelection(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    async def try_sending(self):
        """This command checks if the last role selection embed is still in it's channel. If it isn't, it gets reposted again"""

        ROLES_CHANNEL = self.client.get_channel(self.client.SOMICORD_ROLES_CHANNEL_ID)

        messages = await ROLES_CHANNEL.history(limit=None).flatten()

        if not messages == []:
            return

        self.client.Loggers.action_log(f"Guild: {ROLES_CHANNEL.guild.id} ~ rolelist() generated")

        embed = EmbedFunctions.builder(
            color = self.client.BOT_COLOR,
            title = "Role selection",
            fields = [
                [
                    "Info Roles",
                    f"""
                    Info roles will ping you for a certain event. The currtent info roles are:
                    <@&{self.client.Lists.SOMICORD_UPDATE_ROLES_IDS['UPDATES_ID']}>: Informs you about big news (like a comeback).
                    <@&{self.client.Lists.SOMICORD_UPDATE_ROLES_IDS['LIVE_ID']}>: Informs you about a SNS update.
                    <@&{self.client.Lists.SOMICORD_UPDATE_ROLES_IDS['SNS_ID']}>: Informs you about a live from Somi.
                    <@&{self.client.Lists.SOMICORD_UPDATE_ROLES_IDS['REDDIT_ID']}>: Informs you about a new post on r/Somi.
                    """,
                    False
                ],

                [
                    "How It Works",
                    'Click the button of the role you want down below. If you want to get rid of a role afterwards just click the button again. If you are unsure about your current roles press the button "ROLES".',
                    False
                ]
            ]
        )

        await ROLES_CHANNEL.send(embed=embed, view=Roles(self.client))



def setup(client: SomiBot):
    client.add_cog(RoleSelection(client))