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
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: Interaction):
        self.value = False
        self.stop()

class modmail(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###modmail###########################################################

    @commands.Cog.listener()
    async def on_message(self,
                         message):
        if not isinstance(message.channel, DMChannel):
            return

        if message.author.bot:
            return

        if len(message.content) < 50:
            await message.channel.send("Your modmail must be longer than 50 characters!")
            return

        view = Question_Modmail()
        await message.channel.send("Do you really want to submit this as a modmail?", view=view, delete_after=30)
        await view.wait()

        if not view.value or view.value is None:
            await message.channel.send("Your modmail has **not** been submitted!")
            return

        print(f"{message.author}: modmail()\n{message.content}")

        MOD_CHANNEL = self.client.get_channel(MOD_CHANNEL_ID)
        user_thread = None

        for thread in MOD_CHANNEL.guild.threads:
            if f"{message.author.name}{message.author.discriminator}" in f"{thread.name}":
                user_thread = thread

        if user_thread == None:
            user_thread = await MOD_CHANNEL.create_thread(name = f"Modmail ({message.author})", message = None, auto_archive_duration = 4320, type = nextcord.ChannelType.public_thread) #4320 is 3 days in minutes
            for member in MOD_CHANNEL.members:
                if not member.bot:
                    await user_thread.add_user(member)

        member_avatar_url = get_user_avatar(message.author)

        embed = embed_builder(title = f"Modmail by {message.author}",
                              color = MOD_COLOR,
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "ID:",
                              field_one_value = message.author.id,
                              field_one_inline = True,

                              field_two_name = "Member:",
                              field_two_value = f"{message.author.mention}",
                              field_two_inline = True)

        checks_max_word_length(message, embed, source = "modmail")

        await embed_attachments(user_thread, message, embed)

        await message.channel.send("Your modmail has been submitted!")

        uses_update("command_uses", "modmail")

def setup(client):
    client.add_cog(modmail(client))