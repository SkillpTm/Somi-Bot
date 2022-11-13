###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.partial_commands import get_user_avatar, embed_attachments, embed_builder, deactivate_view_children
from utilities.variables import MOD_CHANNEL_ID, MOD_COLOR

class QuestionModmail(nextcord.ui.View):
    def __init__(self, response):
        self.response: nextcord.Message = response
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        self.value = True
        await deactivate_view_children(self)
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: nextcord.Interaction):
        self.value = False
        await deactivate_view_children(self)
        self.stop()

    async def on_timeout(self):
        await deactivate_view_children(self)

class Modmail(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###modmail###########################################################

    @nextcord.ext.commands.Cog.listener()
    async def on_message(self,
                         message):
        if not isinstance(message.channel, nextcord.DMChannel):
            return

        if message.author.bot:
            return

        if len(message.content) < 50:
            await message.channel.send("Your modmail must be longer than 50 characters!")
            return

        
        response = await message.reply("Do you really want to submit this as a modmail?")
        view = QuestionModmail(response)
        await response.edit("Do you really want to submit this as a modmail?", view=view)
        await view.wait()

        if not view.value or view.value == None:
            await response.reply("Your modmail has **not** been submitted!")
            return

        print(f"{message.author}: modmail()\n{message.content}")

        MOD_CHANNEL = self.client.get_channel(MOD_CHANNEL_ID)
        user_thread = None

        for thread in MOD_CHANNEL.guild.threads:
            if f"{message.author}" in f"{thread.name}":
                user_thread = thread

        if user_thread == None:
            user_thread = await MOD_CHANNEL.create_thread(name = f"Modmail ({message.author})", message = None, auto_archive_duration = 4320, type = nextcord.ChannelType.public_thread) #4320 is 3 days in minutes
            for member in MOD_CHANNEL.members:
                if not member.bot:
                    await user_thread.add_user(member)

        member_avatar_url = get_user_avatar(message.author)

        embed = embed_builder(title = f"Modmail by {message.author}",
                              description = f"__**Message:**__\n{message.content}"[:4096],
                              color = MOD_COLOR,
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "ID:",
                              field_one_value = message.author.id,
                              field_one_inline = True,

                              field_two_name = "Member:",
                              field_two_value = f"{message.author.mention}",
                              field_two_inline = True)

        await embed_attachments(user_thread, message, embed)

        await response.reply("Your modmail has been submitted!")

        uses_update("command_uses", "modmail")



def setup(client):
    client.add_cog(Modmail(client))