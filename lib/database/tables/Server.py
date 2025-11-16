import enum

from lib.database.DataAccess import DataAccessMixin, Table

class Server(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    AUDIT_LOG = "audit_log_id"
    DEFAULT_ROLE = "default_role_id"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "server"

    @staticmethod
    def make_primary_key(key: int | str) -> dict["Server", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Server.ID: key}