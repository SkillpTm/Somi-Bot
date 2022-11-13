###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import REACTION_EMOTE, SOMIONLY_EMOTE, SOMI_F_EMOTE, SOMI_BEST_GRILL_EMOTE, BOT_COLOR
from utilities.partial_commands import get_user_avatar, embed_attachments, message_object_generation, embed_builder



class LinkEmbed(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    @nextcord.ext.commands.Cog.listener()
    async def on_message(self,
                         message: nextcord.Message):
        if not checks(message.guild, message.author):
            return

    ###reaction#on#ping###########################################################

        if self.client.user.mentioned_in(message):
            await message.add_reaction(REACTION_EMOTE)

            print(f"{message.author}: Reacted() @ping")

            uses_update("log_activations", "reacted @ping")

    ###reaction#on#somionly###########################################################

        if "somionly" in str(message.content.lower()):
            await message.add_reaction(SOMIONLY_EMOTE)

            print(f"{message.author}: Reacted() @SOMIONLY")

            uses_update("log_activations", "reacted somionly")

    ###reaction#on#F###########################################################

        f_words = [" f ", SOMI_F_EMOTE.lower()]

        if any(i in f" {message.content.lower()} " for i in f_words):
            await message.add_reaction(SOMI_F_EMOTE)

            print(f"{message.author}: Reacted() @SomiF")

            uses_update("log_activations", "reacted SomiF")

    ###reaction#on#SomiBestGrill###########################################################

        if "<:somibestgrill:924281555772403722>" in str(message.content.lower()):
            await message.add_reaction(SOMI_BEST_GRILL_EMOTE)

            print(f"{message.author}: Reacted() @SomiBestGrill")

            uses_update("log_activations", "reacted SomiBestGrill")

    ###auto#link#embed###########################################################

        if not f"https://discord.com/channels/{message.guild.id}" in str(message.content):
            return

        head, link1, link2 = message.content.partition("https://discord.com/channels/")
        link3 = link1 + link2
        link, body, tail = link3.partition(" ")
        message = await message_object_generation(link, self.client)

        if message.content == "" and len(message.attachments) == 0:
            return

        print(f"{message.author}: Link_Embed()")

        member_avatar_url = get_user_avatar(message.author)

        if len(message.content) < 990:
            message_content = message.content
        else:
            message_content = f"{message.content[:972]}..."

        embed = embed_builder(description = f"{message.channel.mention} - [Link]({link})",
                              color = BOT_COLOR,
                              author = "Message Embed",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = f"{message.author.name} said:",
                              field_one_value = message_content,
                              field_one_inline = False)

        await embed_attachments(message.channel, message, embed, limit = 1)

        uses_update("log_activations", "auto embed")



def setup(client):
    client.add_cog(LinkEmbed(client))