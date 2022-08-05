###package#import###############################################################################

import logging
import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import application_checks, commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs.role_selection.role_selection import roles

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, MOD_COLOR, EXTENSION_FOLDERS
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, restart_bot

###cog#import###############################################################################

for folder in EXTENSION_FOLDERS:
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
    print("Logged in as {0.user}".format(client))
    
    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name='XOXO - The First Album'))
    
    client.add_view(roles())

###restart###############################################################################

@client.slash_command(name="restart", description="restarts the entire bot")
@application_checks.has_any_role(MODERATOR_ID)
async def restart(interaction: Interaction):
    if not checks(interaction):
        return

    print(f"{interaction.user}: /restart")

    AUDIT_LOG = client.get_channel(AUDIT_LOG_ID)
    
    await interaction.response.send_message("Restarting bot...", ephemeral=True)
    
    embed = Embed(colour=MOD_COLOR)
    embed_kst_footer(embed)
    embed_set_mod_author(interaction, embed)
    embed.add_field(name = "/restart:", value = f"{interaction.user.mention} restarted the bot", inline = True)

    await AUDIT_LOG.send(embed=embed)

    uses_update("mod_command_uses", "restart")
    
    restart_bot()

@restart.error
async def restart_error(interaction: Interaction, error):
    await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

###reload###############################################################################
    
@client.slash_command(name="reload", description="reload the entire bot")
@application_checks.has_any_role(MODERATOR_ID)
async def reload(interaction: Interaction):
    if not checks(interaction):
        return

    print(f"{interaction.user}: /reload")

    AUDIT_LOG = client.get_channel(AUDIT_LOG_ID)

    for folder in EXTENSION_FOLDERS:
        for extension in os.listdir(f"./cogs/{folder}/"):
            if extension.endswith(".py"):
                client.reload_extension(f'cogs.{folder}.{extension[:-3]}')
                
    await interaction.response.send_message("The bot has been reloaded", ephemeral=True)

    embed = Embed(colour=MOD_COLOR)
    embed_kst_footer(embed)
    embed_set_mod_author(interaction, embed)
    embed.add_field(name = "/reload:", value = f"{interaction.user.mention} reloaded the bot", inline = True)
    
    await AUDIT_LOG.send(embed=embed)

    uses_update("mod_command_uses", "reload")

@reload.error
async def error(interaction: Interaction, error):
    await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)



client.run(os.getenv('TOKEN'))