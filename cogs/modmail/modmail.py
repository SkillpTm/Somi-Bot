###package#import###############################################################################

import nextcord
from nextcord import Interaction, DMChannel
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks_max_word_length
from utilities.partial_commands import get_user_avatar, embed_attachments, embed_builder
from utilities.variables import MOD_CHANNEL_ID, MOD_COLOR

class Question_Modmail(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: Interaction):
        await interaction.user.send("Your modmail has been submitted!")
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: Interaction):
        await interaction.user.send("Your modmail has **not** been submitted!")
        self.value = False
        self.stop()

class modmail(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###modmail###########################################################

    @commands.Cog.listener()
    async def on_message(self,
                         message):
        if isinstance(message.channel, DMChannel):
            if not message.author.bot:
                if len(message.content) < 50:
                    await message.channel.send("Your modmail must be longer than 50 characters!")
                    return

                elif len(message.content) > 50:

                    view = Question_Modmail()
                    await message.channel.send("Do you really want to submit this as a modmail?", view=view, delete_after=30)
                    await view.wait()

                    MOD_CHANNEL = self.client.get_channel(MOD_CHANNEL_ID)

                    member_avatar_url = get_user_avatar(message.author)

                    embed = embed_builder(title = f"Modmail by {message.author}",
                                          color = MOD_COLOR,
                                          thumbnail = member_avatar_url,

                                          field_one_name = "ID:",
                                          field_one_value = message.author.id,
                                          field_one_inline = True,

                                          field_two_name = "Member:",
                                          field_two_value = f"{message.author.mention}",
                                          field_two_inline = True)

                    checks_max_word_length(message, embed, source = "modmail")

                    if view.value is None:
                        await message.channel.send("Your modmail has **not** been submitted!")
                        return

                    elif view.value:
                        print(f"{message.author}: modmail()\n{message.content}")

                        await embed_attachments(MOD_CHANNEL, message, embed)

                        uses_update("command_uses", "modmail")
                        return
                    elif not view.value:
                        return

def setup(client):
    client.add_cog(modmail(client))