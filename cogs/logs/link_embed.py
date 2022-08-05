###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks, checks_max_word_length
from utilities.variables import REACTION_EMOTE, SOMIONLY_EMOTE, SOMI_F
from utilities.partial_commands import embed_kst_footer, embed_set_message_author, embed_attachments, message_object_generation



class on_message(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,
                         interaction: Interaction):
        if not checks(interaction):
            return

    ###reaction#on#ping###########################################################

        if self.client.user.mentioned_in(interaction):
            await interaction.add_reaction(REACTION_EMOTE)

            print(f"{interaction.author}: Reacted() @ping")

            uses_update("log_activations", "reacted @ping")

    ###reaction#on#somionly###########################################################

        if "somionly" in str(interaction.content.lower()):
            await interaction.add_reaction(SOMIONLY_EMOTE)

            print(f"{interaction.author}: Reacted() @SOMIONLY")

            uses_update("log_activations", "reacted somionly")

    ###reaction#on#F###########################################################

        f_words = [" f ", SOMI_F.lower()]

        if any(i in f" {interaction.content.lower()} " for i in f_words):
            await interaction.add_reaction(SOMI_F)

            print(f"{interaction.author}: Reacted() @SomiF")

            uses_update("log_activations", "reacted SomiF")

    ###auto#link#embed###########################################################

        if f"https://discord.com/channels/{interaction.guild.id}" in str(interaction.content):

            print(f"{interaction.author}: Link_Embed()")

            head, link1, link2 = interaction.content.partition("https://discord.com/channels/")
            link3 = link1 + link2
            link, body, tail = link3.partition(" ")
            message ,correct_channel = await message_object_generation(link, self.client)

            embed = Embed(description= f"{correct_channel.mention} - [Link]({link})",
                          colour=nextcord.Color.from_rgb(255, 166, 252))
            embed_kst_footer(embed)
            embed_set_message_author(message, embed, "Message Embed")
            checks_max_word_length(message, embed, source = "link_embed")

            await embed_attachments(interaction.channel, message, embed, link_embed = True)

            uses_update("log_activations", "auto embed")

def setup(client):
    client.add_cog(on_message(client))