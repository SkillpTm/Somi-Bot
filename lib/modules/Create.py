import csv
import nextcord



class Create():

    def __init__(self) -> None:
        pass

    ####################################################################################################
    
    @staticmethod
    def bulk_messages_csv(messages: list[nextcord.Message]) -> None:
        """This function creates a CSV file, which saves the author id/name, the time and the content of messages"""

        messages.reverse()
        fieldnames = ["Author ID", "Author Name", "Send at", "Content"]

        with open(f"./storage/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{len(messages)}.csv", "w") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
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