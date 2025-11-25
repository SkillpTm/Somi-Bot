import html

from google.api_core import exceptions
import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain
from lib.modules import SomiBot



class Translate(nextcord_C.Cog):

    languages_name_key: dict[str, str] = {lang["name"]: lang["language"] for lang in Keychain().translator.get_languages()}
    languages_key_name: dict[str, str] = {lang["language"]: lang["name"] for lang in Keychain().translator.get_languages()}


    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["translate"].name,
        Commands().data["translate"].description,
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def translate(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        text: str = nextcord.SlashOption(
            Commands().data["translate"].parameters["text"].name,
            Commands().data["translate"].parameters["text"].description,
            required = True,
            min_length = 2,
            max_length = 500
        ),
        new_lang: str = nextcord.SlashOption(
            Commands().data["translate"].parameters["new_lang"].name,
            Commands().data["translate"].parameters["new_lang"].description,
            required = False,
            min_length = 2,
            max_length = 50,
            default = "en"
        ),
        old_lang: str = nextcord.SlashOption(
            Commands().data["translate"].parameters["old_lang"].name,
            Commands().data["translate"].parameters["old_lang"].description,
            required = False,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """Translates text from one language to another using Google Translate API"""

        if (new_lang not in self.languages_key_name.keys()) or (old_lang and old_lang not in self.languages_key_name.keys()):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"The language `{new_lang}` is not supported!"), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        try:
            result: dict[str, str] = Keychain().translator.translate(text, target_language=new_lang, source_language=old_lang if old_lang else None)
            old_lang = old_lang if old_lang else result["detectedSourceLanguage"]
        except exceptions.Forbidden:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("The daily API qouta was exceded, please try tomorrow again."))
            return

        embed = EmbedFunctions.builder(
            color = Config().TRANSLATE_COLOR,
            author = f"{self.languages_key_name[old_lang]} --> {self.languages_key_name[new_lang]}",
            author_url = f"https://translate.google.com/?sl={old_lang}&tl={new_lang}",
            author_icon = Config().TRANSLATE_ICON,
            description = f"## **Original Text ({old_lang}):**\n{text}\n**## Translated Text ({new_lang}):**```{html.unescape(result['translatedText'])}```",
        )

        await interaction.send(embed=embed)


    @translate.on_autocomplete("new_lang")
    async def translate_autocomplete_new_lang(self, interaction: nextcord.Interaction[SomiBot], new_lang: str) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(Get.autocomplete(new_lang, self.languages_name_key))


    @translate.on_autocomplete("old_lang")
    async def translate_autocomplete_old_lang(self, interaction: nextcord.Interaction[SomiBot], old_lang: str) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(Get.autocomplete(old_lang, self.languages_name_key))



def setup(client: SomiBot) -> None:
    client.add_cog(Translate(client))