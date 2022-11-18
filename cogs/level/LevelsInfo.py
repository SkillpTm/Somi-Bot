###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_levels_ignore import ignore_channels_list
from database.database_levelroles import get_server_level_roles
from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import BOT_COLOR



class LevelsInfo(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import levels

    ###level#roles#info###########################################################

    @levels.subcommand(name = "info", description = "a list and explanation for levelroles")
    async def levels_info(self,
                          interaction: nextcord.Interaction):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /levels info")

        levelroles = get_server_level_roles(interaction.guild.id)
        output_role_list = ""
        output_ignore_channels = ""

        for levelrole in levelroles:
            output_role_list += f"Level >{levelrole[1]-1}: <@&{levelrole[0]}>\n"

        if output_role_list == "":
            output_role_list = "This server has no levelroles!"

        ignore_channel_ids = ignore_channels_list(interaction.guild.id)

        for channel_id in ignore_channel_ids:
            output_ignore_channels += f"<#{channel_id}>\n"

        embed = embed_builder(title = "Level Roles",
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "What are level roles?",
                              field_one_value = "If you send a message you receive a few xp points. These xp points will eventually make you level up and at certain levels you get level roles. You can see your level by using `_level`",
                              field_one_inline = False,

                              field_two_name = "Role list:",
                              field_two_value = output_role_list,
                              field_two_inline = False,
                              
                              field_three_name = "No XP Channels:",
                              field_three_value = output_ignore_channels,
                              field_three_inline = False)

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "levels info")



def setup(client):
    client.add_cog(LevelsInfo(client))