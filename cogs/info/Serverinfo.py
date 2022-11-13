###package#import###############################################################################

import nextcord
import time

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import DEFAULT_PFP, BOT_COLOR



class Severinfo(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###serverinfo###########################################################
        
    @nextcord.slash_command(name = "si", description = "gives information about this server", name_localizations = {country_tag:"serverinfo" for country_tag in nextcord.Locale})
    async def serverinfo(self,
                         interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /serverinfo")

        created_time = int(time.mktime(interaction.guild.created_at.timetuple()))

        guild_with_counts = await client.fetch_guild(interaction.guild.id, with_counts=True)

        if interaction.guild.icon is not None:
            server_icon_url = interaction.guild.icon
        else:
            server_icon_url = DEFAULT_PFP

        embed = embed_builder(title = f"Server Information: `{interaction.guild.name}`",
                            color = BOT_COLOR,
                            thumbnail = server_icon_url,
                            footer = "DEFAULT_KST_FOOTER",

                            field_one_name = "ID:",
                            field_one_value = interaction.guild.id,
                            field_one_inline = False,
                                                
                            field_two_name = "Owner:",
                            field_two_value = interaction.guild.owner.mention,
                            field_two_inline = True,
                                                
                            field_three_name = "Members:",
                            field_three_value = f"Total: {interaction.guild.member_count}\nOnline: {guild_with_counts.approximate_presence_count}",
                            field_three_inline = True,
                                                
                            field_four_name = "Channels:",
                            field_four_value = f"Text: {len(interaction.guild.text_channels)}\nVoice: {len(interaction.guild.voice_channels)}",
                            field_four_inline = True,
                                                
                            field_five_name = "Created at:",
                            field_five_value = f"<t:{created_time}>",
                            field_five_inline = True)

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "serverinfo")



def setup(client):
    client.add_cog(Severinfo(client))