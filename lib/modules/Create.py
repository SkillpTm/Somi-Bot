import csv
import nextcord



class Create():

    def __init__(self) -> None:
        pass

    ####################################################################################################
    
    @staticmethod
    def bulk_messages_csv(messages: list[nextcord.Message]) -> str:
        """This function creates a CSV file, which saves the author id/name, the time and the content of messages. It returns the file name of this CSV."""

        # discord provides the message in chronological order, we want the latest first though
        messages.reverse()
        # the file, while temporary, is supposed to have a unique name, in case someone purges at the same time
        file_name = f"./debug/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{messages[0].id}_{len(messages)}.csv"

        with open(file_name, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["Author ID", "Author Name", "Send at", "Content"])
            writer.writeheader()

            for message in messages:
                message_sent_time = message.created_at.strftime("%Y/%m/%d %H:%M:%S")

                writer.writerow(
                    {
                        "Author ID": message.author.id,
                        "Author Name": message.author.display_name,
                        "Send at": message_sent_time,
                        "Content": message.content
                    }
                )

        return file_name