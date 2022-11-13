###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import MODERATOR_ID, RULES



class Rules(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###rules###########################################################

    @nextcord.slash_command(name = "rules", description = "[MOD] posts a rule for you")
    @nextcord.ext.application_checks.has_permissions(manage_guild=True)
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
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /rules {rule}")

        embed = embed_builder(description = RULES[rule][0],
                              color = nextcord.Color.red(),
                              author = f"Rule {rule}",
                              author_icon = interaction.guild.icon,                
                              footer = RULES[rule][1])
        
        await interaction.response.send_message(embed=embed)

        uses_update("mod_command_uses", "rules")

    @rules.error
    async def purge_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Rules(client))