import enum

from lib.database.DataAccess import DataAccessMixin, Table

class Statistic(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    USER = "user"
    SERVER = "server"
    ATTACHMENTS = "attachment_count"
    CHARS = "char_count"
    COMMANDS = "command_count"
    EMOTES = "emote_count"
    LINKS = "link_count"
    MESSAGES = "message_count"
    REPLIES = "reply_count"
    STICKERS = "sticker_count"
    WORDS = "word_count"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "statistic"

    @staticmethod
    def make_primary_key(key: int | str) -> dict["Statistic", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Statistic.ID: key}