from lib.database.DataAccess import DataAccessMixin, Table
from lib.database.Database import Database
from lib.database.Query import Query



class Statistic(DataAccessMixin):
    ID = "id"
    USER = "user"
    SERVER = "server"
    ATTACHMENTS = "attachment_count"
    CHARS = "char_count"
    COMMANDS = "bot_command_count"
    DELETES = "delete_count"
    EDITS = "edit_count"
    EMOTES = "emote_count"
    LINKS = "link_count"
    MESSAGES = "message_count"
    REACTIONS = "reaction_count"
    REPLIES = "reply_count"
    STICKERS = "sticker_count"
    WORDS = "word_count"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "statistic"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Statistic.ID: key}


    async def increase(self, where: dict[Table, int | str | None] | int | str | None, data: dict[Table, int | str | None] | int | str | None) -> bool:
        """increases statistic value(s) and adds a new row if it does not exist"""

        if not isinstance(data, dict):
            data = {self: data}

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        await self.add_unique(where, {Statistic.USER: where.get(Statistic.USER), Statistic.SERVER: where.get(Statistic.SERVER)} | data)

        return await Database().execute(
            Statistic.get_table(),
            Query.STATISTIC_INCREASE,
            data = {key.value: value for key, value in data.items()},
            where = {key.value: value for key, value in where.items()}
        )