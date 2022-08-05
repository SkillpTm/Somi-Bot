###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_message_author
from utilities.variables import UPDATES_ID, LIVE_ID, SNS_ID, REDDIT_ID, ROLES_ID, BOT_COLOR, ROLELIST



class roles(nextcord.ui.View):
    
    def __init__(self):
        super().__init__(timeout=None)

    async def handle_click(self,
                           button: nextcord.ui.button,
                           interaction: Interaction):
        if not checks(interaction):
            return

        role_id, sep, role_name = button.custom_id.partition(".")
        role = interaction.guild.get_role(int(role_id))

        if role in interaction.user.roles:
            print(f"{interaction.user}: rolelist() remove {role}")

            uses_update("role_selections", f"remove {role.name}")

            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"The role: {role.mention} has been removed form your role list", ephemeral=True)
        else:
            print(f"{interaction.user}: rolelist() add {role.name}")

            uses_update("role_selections", f"add {role}")

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"The role: {role.mention} has been added to your role list", ephemeral=True)


    @nextcord.ui.button(label = "UPDATES", style=nextcord.ButtonStyle.blurple, custom_id=f"{UPDATES_ID}.{ROLELIST[UPDATES_ID]}")
    async def UPDATES(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "LIVE", style=nextcord.ButtonStyle.blurple, custom_id=f"{LIVE_ID}.{ROLELIST[LIVE_ID]}")
    async def LIVE(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "SNS", style=nextcord.ButtonStyle.blurple, custom_id=f"{SNS_ID}.{ROLELIST[SNS_ID]}")
    async def SNS(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "REDDIT", style=nextcord.ButtonStyle.blurple, custom_id=f"{REDDIT_ID}.{ROLELIST[REDDIT_ID]}")
    async def REDDIT(self, button: nextcord.ui.Button, interaction: Interaction):
        await self.handle_click(button, interaction)

    @nextcord.ui.button(label = "ROLES", style=nextcord.ButtonStyle.gray, custom_id="JeonSomi.ROLES")
    async def ROLES(self, button: nextcord.ui.Button, interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: rolelist() ROLES")

        rolelist = [i.mention for i in interaction.user.roles if i != interaction.guild.default_role]
        output = ""
        
        embed = Embed(colour=BOT_COLOR)
        embed_kst_footer(embed)
        embed_set_message_author(interaction, embed, title_name = f"Rolelist for {interaction.user}")

        for i in range(len(rolelist)):
            output += f"{i + 1}. {rolelist[i]}\n"
        embed.add_field(name = "Roles:", value = f"{output[:1000]}", inline = True)

        await interaction.send(embed=embed, ephemeral=True)

        uses_update("role_selections", "clicked ROLES")


class role_selection(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###roleselection#generation###########################################################

    @commands.Cog.listener()
    async def on_ready(self):
        ROLES_CHANNEL = self.client.get_channel(ROLES_ID)

        messages = await ROLES_CHANNEL.history(limit=100).flatten()

        if messages == []:
            print("roelist() generated")

            embed = Embed(title="Role selection",
                          colour=BOT_COLOR)
            embed.add_field(name = "Info Roles", value = f"Info roles will ping you for a certain event. The currtent info roles are:\n<@&{UPDATES_ID}>: Informs you about big news (like a comeback).\n<@&{LIVE_ID}>: Informs you about a SNS update.\n<@&{SNS_ID}>: Informs you about a live from Somi.\n<@&{REDDIT_ID}>: Informs you about a new post on r/Somi.", inline = False)
            embed.add_field(name = "How It Works", value = 'Click the button of the role you want down below. If you want to get rid of a role afterwards just click the button again. If you are unsure about your current roles press the button "ROLES".', inline = False)

            await ROLES_CHANNEL.send(embed=embed, view=roles())
        else:
            return

def setup(client):
    client.add_cog(role_selection(client))