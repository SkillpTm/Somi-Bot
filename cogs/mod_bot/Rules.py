####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Rules(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "rules", description = "posts a rule for you", guild_ids = [SomiBot.SOMICORD_ID], default_member_permissions=nextcord.Permissions(manage_guild=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def rules(self,
                    interaction: nextcord.Interaction,
                    *,
                    rule: str = nextcord.SlashOption(description="rule you want to post", required=True, choices=["1 NSFW Content",
                                                                                                                  "2 Doxxing",
                                                                                                                  "3 Cursing",
                                                                                                                  "4 Language",
                                                                                                                  "5 Discrimination",
                                                                                                                  "6 Channel Use",
                                                                                                                  "7 Unboxing Spoiler Tags",
                                                                                                                  "8 Spam",
                                                                                                                  "9 Negativity",
                                                                                                                  "10 Selfpromotion",
                                                                                                                  "11 Relationships"])):
        """This command let's you post an embed for the specified rule."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /rules {rule}")

        await interaction.response.defer(with_message=True)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.red(),
            author = f"Rule {rule}",
            author_icon = interaction.guild.icon, 
            description = self.client.Lists.SOMICORD_RULES[rule][0],               
            footer = self.client.Lists.SOMICORD_RULES[rule][1]
        )
        
        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Rules(client))