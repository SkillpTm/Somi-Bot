import math
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import PageButtons, SomiBot



class ReminderList(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.reminder.subcommand(Commands().data["reminder list"].name, Commands().data["reminder list"].description)
    async def reminder_list(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command will list all reminders of a user"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (all_reminders := typing.cast(list[dict[str, int | str]], await db.Reminder._.get_all(
            [db.Reminder.ID, db.Reminder.MESSAGE, db.Reminder.LINK, db.Reminder.TIME],
            {db.Reminder.USER: interaction.user.id},
            db.Reminder.TIME,
            Order.ASCENDING
        ))):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return

        #     output += f"<t:{db.Reminder.TIME.retrieve(entry)}:F> // ID: {db.Reminder.ID.retrieve(entry)} - [Link]({db.Reminder.LINK.retrieve(entry)})\nReminder: `{reminder_text}`\n\n"

        await self.reminder_list_rec(interaction, all_reminders, 1)


    async def reminder_list_rec(self, interaction: nextcord.Interaction[SomiBot], all_reminders: list[dict[str, int | str]], page: int) -> None:
        """This function is used to paginate through the reminder list"""

        output: list[str] = []

        for index, entry in enumerate(all_reminders[10*(page-1):]):
            if len(output) >= 10:
                break

            text = str(db.Reminder.MESSAGE.retrieve(entry))
            text = f"{text[:100]}..." if len(text) > 100 else text

            output.append(f"`{index+1 + 10*(page-1)}.` [{db.Reminder.ID.retrieve(entry)}]({db.Reminder.LINK.retrieve(entry)}): <t:{db.Reminder.TIME.retrieve(entry)}:f>\n{text}")

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Reminders for {interaction.user.display_name}",
            author_icon = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP,
            description = "\n\n".join(output)
        )

        view = PageButtons(page, math.ceil(len(all_reminders)/10), interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.reminder_list_rec(interaction, all_reminders, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(ReminderList(client))