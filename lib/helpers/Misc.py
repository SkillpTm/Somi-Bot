import csv
import nextcord



class Misc():
    """Helper class with misc methodes"""

    ####################################################################################################

    @staticmethod
    async def deactivate_view_children(button_view: nextcord.ui.View) -> None:
        """This function deactivates all children from a view (buttons/select boxes)"""

        # disable all buttons from this view
        for child in button_view.children:
            child.disabled = True

        response: nextcord.Message = getattr(button_view, "response")
        interaction: nextcord.Interaction = getattr(button_view, "interaction")

        # edit the original class to have its buttons deactivated
        if response:
            await response.edit(view=button_view)
        elif interaction:
            await interaction.edit_original_message(view=button_view)

    ####################################################################################################

    @staticmethod
    def make_bulk_messages_csv(messages: list[nextcord.Message]) -> str:
        """This function creates a CSV file, which saves the author id/name, the time and the content of messages. It returns the file name of this CSV."""

        # discord provides the message in chronological order, we want the latest first though
        messages.reverse()
        # the file, while temporary, is supposed to have a unique name, in case someone purges at the same time
        file_name = f"./debug/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{messages[0].id}_{len(messages)}.csv"

        with open(file_name, "w", encoding="UTF-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Author ID", "Author Name", "Send at", "Content"])
            writer.writeheader()

            for message in messages:
                writer.writerow({
                    "Author ID": message.author.id,
                    "Author Name": message.author.display_name,
                    "Send at": message.created_at.strftime("%Y/%m/%d %H:%M:%S"),
                    "Content": message.content
                })

        return file_name