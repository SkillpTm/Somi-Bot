import nextcord
import nextcord.ext.commands as nextcord_C

from lib.db_modules import CommandUsesDB
from lib.modules import EmbedFunctions, Get
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

        SOMICORD = self.client.get_guild(self.client.SOMICORD_ID)

        if not SOMICORD.get_member(message.author.id):
            return

        if len(message.content) < 50:
            await message.channel.send(embed=EmbedFunctions().error("Your modmail must be longer than 50 characters! Please describe your problem precisely!"))
            return
        
        response = await message.reply(embed=EmbedFunctions().info_message("Do you really want to submit this as a modmail?", self.client), mention_author=False)
        view = YesNoButtons(response=response)
        await response.edit(embed=response.embeds[0], view=view, delete_after=70)
        await view.wait()

        if not view.value:
            await response.reply(embed=EmbedFunctions().error("Your modmail has **not** been submitted!"), mention_author=False)
            return

        self.client.Loggers.action_log(Get().log_message(message, "modmail", {"message": message.content}))

        MOD_CHANNEL: nextcord.TextChannel = self.client.get_channel(self.client.SOMICORD_MOD_CHANNEL_ID)
        user_thread: nextcord.Thread = None

        # check if the user already has a thread
        for thread in MOD_CHANNEL.threads:
            if f"Modmail ({message.author.global_name})" == thread.name[9:-1]:
                user_thread = thread

        # check if the user already has an archived thread
        if not user_thread:
            async for thread in MOD_CHANNEL.archived_threads():
                if f"Modmail ({message.author.global_name})" == thread.name[9:-1]:
                    user_thread = thread

        # if the user doesn't already have a thread, make one
        if not user_thread:
            user_thread = await MOD_CHANNEL.create_thread(
                name = f"Modmail ({message.author})",
                message = None,
                auto_archive_duration = 4320, #4320 is 3 days in minutes
                type = nextcord.ChannelType.public_thread
            )

            for member in MOD_CHANNEL.members:
                if not member.bot and member.id != 108218817531887616: # exclude inactive owner
                    await user_thread.add_user(member)

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            thumbnail = message.author.display_avatar.url,
            title = f"Modmail by {message.author.display_name}",
            description = f"__**Message:**__\n{message.content}"[:4096],
            footer = "DEFAULT_KST_FOOTER",
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

        embed, file_urls = EmbedFunctions().get_attachments(message.attachments, embed)

        sent_modmail = await user_thread.send(embed=embed)
        
        if file_urls:
            await sent_modmail.reply(content=file_urls, mention_author=False)

        await message.reply(embed=EmbedFunctions().success("Your modmail has been submitted!"), mention_author=False)

        CommandUsesDB("command_uses").update("modmail")



def setup(client: SomiBot) -> None:
    client.add_cog(Modmail(client))