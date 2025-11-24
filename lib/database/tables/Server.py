import enum

from lib.database.DataAccess import DataAccessMixin, Table



class Server(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    DEFAULT_ROLE = "default_role_id"
    BAN_LOG = "ban_log"
    COMMAND_LOG = "bot_command_log"
    DELETE_LOG = "delete_log"
    EDIT_LOG = "edit_log"
    JOIN_LOG = "join_log"
    KICK_LOG = "kick_log"
    LEAVE_LOG = "leave_log"
    MUTE_LOG = "mute_log"
    NAME_LOG = "name_log"
    PURGE_LOG = "purge_log"
    REMOVE_LOG = "remove_log"
    UNBAN_LOG = "unban_log"
    UNMUTE_LOG = "unmute_log"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "server"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Server.ID: key}

    @staticmethod
    def get_log_types() -> list["Server"]:
        """returns all log types"""

        return [
            Server.BAN_LOG,
            Server.COMMAND_LOG,
            Server.DELETE_LOG,
            Server.EDIT_LOG,
            Server.JOIN_LOG,
            Server.KICK_LOG,
            Server.LEAVE_LOG,
            Server.MUTE_LOG,
            Server.NAME_LOG,
            Server.PURGE_LOG,
            Server.REMOVE_LOG,
            Server.UNBAN_LOG,
            Server.UNMUTE_LOG
        ]