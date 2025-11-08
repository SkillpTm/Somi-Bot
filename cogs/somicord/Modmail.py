import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.managers import Config, Logger
from lib.modules import EmbedFunctions
from lib.utilities import SomiBot, YesNoButtons



class Modmail(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    async def modmail(self, message: nextcord.Message) -> None:
        """
        This function allows anyone, who is in Somicord send a modmail via the bot pm channel, if:
        - their messageis longer than 50 characters
        - they press the "yes" button within 30 second
        """

        if not isinstance(message.channel, nextcord.DMChannel):
            return

        if message.author.bot:
            return

        if not self.client.get_guild(Config().MODMAIL_SERVER_ID).get_member(message.author.id):
            return

        if len(message.content) < 50:
            await message.channel.send(embed=EmbedFunctions().get_error_message("Your modmail must be longer than 50 characters! Please describe your problem precisely!"))
            return

        response = await message.reply(embed=EmbedFunctions().get_info_message("Do you really want to submit this as a modmail?", self.client), mention_author=False)
        view = YesNoButtons(response=response)
        await response.edit(embed=response.embeds[0], view=view, delete_after=70)
        await view.wait()

        if not view.value:
            await response.reply(embed=EmbedFunctions().get_error_message("Your modmail has **not** been submitted!"), mention_author=False)
            return

        Logger().action_log(message, "modmail", {"message": message.content})

        modmail_channel: nextcord.TextChannel = self.client.get_channel(Config().MODMAIL_CHANNEL_ID)
        user_thread: nextcord.Thread = None

        # check if the user already has a thread
        for thread in modmail_channel.threads:
            if f"Modmail ({message.author.name})" == thread.name[9:-1]:
                user_thread = thread

        # check if the user already has an archived thread
        if not user_thread:
            async for thread in modmail_channel.archived_threads():
                if f"Modmail ({message.author.name})" == thread.name[9:-1]:
                    user_thread = thread

        # if the user doesn't already have a thread, make one
        if not user_thread:
            user_thread = await modmail_channel.create_thread(
                name = f"Modmail ({message.author})",
                message = None,
                auto_archive_duration = 4320, #4320 is 3 days in minutes
                type = nextcord.ChannelType.public_thread
            )

            for member in modmail_channel.members:
                if not member.bot and member.id != 108218817531887616: # exclude inactive owner
                    await user_thread.add_user(member)

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            thumbnail = message.author.display_avatar.url,
            title = f"Modmail by {message.author.display_name}",
            description = f"__**Message:**__\n{message.content}"[:4096],
            footer_icon = Config().CLOCK_ICON,
            footer_timestamp = message.created_at,
            fields = [
                [
                    "ID:",
                    message.author.id,
                    True
                ],

                [
                    "Member:",
                    f"{message.author.mention}",
                    True
                ]
            ]
        )

        embed, file_urls = EmbedFunctions.get_or_add_attachments(message.attachments, embed)

        sent_modmail = await user_thread.send(embed=embed)

        if file_urls:
            await sent_modmail.reply(content=file_urls, mention_author=False)

        await message.reply(embed=EmbedFunctions().get_success_message("Your modmail has been submitted!"), mention_author=False)

        await (await DBHandler(self.client.database).telemetry()).increment("modmail send")



def setup(client: SomiBot) -> None:
    client.add_cog(Modmail(client))