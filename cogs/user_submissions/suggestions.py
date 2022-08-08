###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_bugs_suggestions import submit_suggestion
from utilities.maincommands import checks
from utilities.partial_commands import get_kst_time_stamp



class SuggestionsSubmissionModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Please submit your suggestion down below!", timeout=None)

        self.suggestion: str = nextcord.ui.TextInput(
            label="Suggestion:",
            style=nextcord.TextInputStyle.paragraph,
            min_length=1,
            max_length=4000,
            placeholder="write your suggstion here",
            required=True)

        self.add_item(self.suggestion)

    async def callback(self, interaction: Interaction):
        kst_timestamp = get_kst_time_stamp(source = "/suggestions")

        print(f"{interaction.user}: /suggestions submission:\n{self.suggestion.value}")

        server_id = interaction.guild.id
        user_id = interaction.user.id
        user_name = str(interaction.user)
        submission_time = kst_timestamp
        bug_report = self.suggestion.value

        submit_suggestion(server_id, user_id, user_name.replace("'", "‘"), submission_time, bug_report.replace("'", "‘"))

        await interaction.response.send_message("Your suggestion has been submitted!", ephemeral=True)

        uses_update("command_uses", "suggestions")

        return

class suggestions(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###suggestions###########################################################

    @nextcord.slash_command(name = "suggestions", description = "Make a private suggestion")
    async def suggestions(self,
                          interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /suggestions")

        SuggestionModal = SuggestionsSubmissionModal()
        await interaction.response.send_modal(modal=SuggestionModal)

def setup(client):
    client.add_cog(suggestions(client))