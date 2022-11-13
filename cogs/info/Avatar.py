###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_nick_else_name, get_user_avatar, embed_builder
from utilities.variables import BOT_COLOR



class Avatar(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###avatar###########################################################

    @nextcord.slash_command(name = "avatar", description = "posts someone's avatar")
    async def avatar(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want the avatar from", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /avatar {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        
        member_avatar_url = get_user_avatar(member)

        name = get_nick_else_name(member)

        embed = embed_builder(title = f"Avatar of: `{name}`",
                              title_url = member_avatar_url,
                              color = BOT_COLOR,
                              image = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER")

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "avatar")



def setup(client):
    client.add_cog(Avatar(client))