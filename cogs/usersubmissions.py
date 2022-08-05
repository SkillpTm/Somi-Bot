import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from datetime import datetime
from pytz import timezone

intents = nextcord.Intents.default()
intents.members = True

client = commands.Bot(intents=intents)

class usersubmissions(commands.Cog):

  def __init__(self, client):
    self.client = client

  ###suggestions###########################################################

  @nextcord.slash_command(name = "suggestions", description = "Make a private suggestion")
  async def suggestions(self, interaction: Interaction, *, suggestion = SlashOption(description="The suggestion you want to make", required=True)):
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    suggestions = open("./storage/suggestions.txt", "a")
    suggestions.write("Name: " + str(interaction.user) + "\n" +
                      "ID: " + str(interaction.user.id) + "\n" +
                      "Time: " + now_korea.strftime(format) + "\n" +
                      "Suggestion: " + str(suggestion)+ "\n"
                      "##############################################################" + "\n")
    suggestions.close()
    await interaction.response.send_message("Your suggestion has been submitted!", ephemeral=True)

  ###bugs###########################################################

  @nextcord.slash_command(name = "bugs", description = "Report a bug")
  async def bugs(self, interaction: Interaction, *, bug = SlashOption(description="The bug you want to report", required=True)):
    format = "%Y/%m/%d %H:%M:%S %Z"
    now_utc = datetime.now(timezone('UTC'))
    now_korea = now_utc.astimezone(timezone('Asia/Seoul'))
    bugs = open("./storage/bugs.txt", "a")
    bugs.write("Name: " + str(interaction.user) + "\n" +
               "ID: " + str(interaction.user.id) + "\n" +
               "Time: " + now_korea.strftime(format) + "\n" +
               "Bug: " + str(bug)+ "\n"
               "##############################################################" + "\n")
    bugs.close()
    await interaction.response.send_message("Your bug-report has been submitted!", ephemeral=True)

def setup(client):
  client.add_cog(usersubmissions(client))