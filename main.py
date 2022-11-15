###package#import###############################################################################

import dotenv
import logging
import nextcord
import nextcord.ext.commands
import nextcord.ext.application_checks
import os

dotenv.load_dotenv()

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs.role_selection.RoleSelection import Roles

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR
from utilities.partial_commands import get_user_avatar, restart_bot, embed_builder

###cog#import###############################################################################

for folder in os.listdir(f"./cogs/"):
    if os.path.isdir(f"./cogs/{folder}/"):
        for extension in os.listdir(f"./cogs/{folder}/"):
            if extension.endswith(".py"):
                client.load_extension(f"cogs.{folder}.{extension[:-3]}")

###error#log###############################################################################

logger = logging.getLogger('nextcord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='./storage/error.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

###on#ready###############################################################################

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='XOXO - The First Album'))
    
    client.add_view(Roles())

###restart###############################################################################

@client.slash_command(name="restart", description="[MOD] restarts the entire bot")
@nextcord.ext.application_checks.has_any_role(MODERATOR_ID)
async def restart(interaction: nextcord.Interaction):
    if not checks(interaction.guild, interaction.user):
        return

    print(f"{interaction.user}: /restart")

    AUDIT_LOG = client.get_channel(AUDIT_LOG_ID)
    member_avatar_url = get_user_avatar(interaction.user)
    
    await interaction.response.send_message("Restarting bot...", ephemeral=True)

    embed = embed_builder(color = MOD_COLOR,
                          author = "Mod Activity",
                          author_icon = member_avatar_url,

                          field_one_name = "/restart:",
                          field_one_value = f"{interaction.user.mention} restarted the bot!",
                          field_one_inline = True)

    await AUDIT_LOG.send(embed=embed)

    uses_update("mod_command_uses", "restart")
    
    restart_bot()

@restart.error
async def restart_error(interaction: nextcord.Interaction, error):
    await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

###reload###############################################################################
    
@client.slash_command(name="reload", description="[MOD] reload the entire bot")
@nextcord.ext.application_checks.has_any_role(MODERATOR_ID)
async def reload(interaction: nextcord.Interaction):
    if not checks(interaction.guild, interaction.user):
        return

    print(f"{interaction.user}: /reload")

    for folder in os.listdir(f"./cogs/"):
        if os.path.isdir(f"./cogs/{folder}/"):
            for extension in os.listdir(f"./cogs/{folder}/"):
                if extension.endswith(".py"):
                    client.reload_extension(f'cogs.{folder}.{extension[:-3]}')

    await client.sync_all_application_commands()
                
    await interaction.response.send_message("The bot has been reloaded.", ephemeral=True)

    AUDIT_LOG = client.get_channel(AUDIT_LOG_ID)
    member_avatar_url = get_user_avatar(interaction.user)

    embed = embed_builder(color = MOD_COLOR,
                          author = "Mod Activity",
                          author_icon = member_avatar_url,

                          field_one_name = "/reload:",
                          field_one_value = f"{interaction.user.mention} reloaded the bot!",
                          field_one_inline = True)
    
    await AUDIT_LOG.send(embed=embed)

    uses_update("mod_command_uses", "reload")

@reload.error
async def error(interaction: nextcord.Interaction, error):
    await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



client.run(os.getenv("DISCORD_TOKEN"))