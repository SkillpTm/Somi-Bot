###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_get_title_name
from utilities.variables import BOT_COLOR



class banner(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###banner###########################################################

    @nextcord.slash_command(name="banner", description = "posts someone's banner")
    async def banner(self,
                     interaction: Interaction,
                     *,
                     member: nextcord.Member = SlashOption(description="The user you want the banner from (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /banner {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        user = await self.client.fetch_user(member.id)

        title_name = embed_get_title_name(member)

        try:
            if user.banner.url is None:
                await interaction.response.send_message(f"The user `{title_name}` doesn't have a banner", ephemeral=True)
                return
        except:
            await interaction.response.send_message(f"The user `{title_name}` doesn't have a banner", ephemeral=True)
            return
            
        embed = Embed(title= f"Banner of: `{title_name}`",
                      url = user.banner.url,
                      colour=BOT_COLOR)
        embed_kst_footer(embed)

        embed.set_image(url=user.banner.url)

        await interaction.send(embed=embed)

        uses_update("command_uses", "banner")

def setup(client):
    client.add_cog(banner(client))