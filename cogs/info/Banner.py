###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, embed_builder
from utilities.variables import BOT_COLOR



class Banner(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###banner###########################################################

    @nextcord.slash_command(name = "banner", description = "posts someone's banner")
    async def banner(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want the banner from", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /banner {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        user = await self.client.fetch_user(member.id)

        name = get_nick_else_name(member)

        try:
            if user.banner.url == None:
                await interaction.response.send_message(f"The user `{name}` doesn't have a banner.", ephemeral=True)
                return
        except:
            await interaction.response.send_message(f"The user `{name}` doesn't have a banner.", ephemeral=True)
            return

        embed = embed_builder(title = f"Banner of: `{name}`",
                              title_url = user.banner.url,
                              color = BOT_COLOR,
                              image = user.banner.url,
                              footer = "DEFAULT_KST_FOOTER")
        
        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "banner")



def setup(client):
    client.add_cog(Banner(client))