import enum



class Order(enum.Enum):
    ASCENDING = "ASC"
    DESCENDING = "DESC"
    NONE = ""

class Query(enum.Enum):
    DELETE = "delete_where"
    INSERT = "insert"
    SELECT = "select_where"
    UPDATE = "update_where"

    INSERT_UNIQUE = "insert_unique"
    TELENETRY_INCREMENT = "telemetry_increment"
    USER_RANK = "user_rank"

    def formated(
        self,
        queries: dict[str, str],
        table: str = "",
        *,
        data: dict[str, str] = {},
        select: list[str] = [],
        where: dict[str, str] = [],
        order_by: str = None,
        order: Order = Order.NONE,
        limit: int = 1
    ) -> str:
        """Formats the query string based on the type of query and provided parameters."""

        query = queries[self.value]
        query = query.replace(":_table", table)
        query = query.replace(":_columns", ", ".join(data.keys())).replace(":_values", ", ".join(["%s"] * len(data)))
        query = query.replace(":_selects", ", ".join(select))
        query = query.replace(":_where_columns", ", ".join(where.keys())).replace(":_where_values", ", ".join(["%s"] * len(where)))
        query = query.replace(":_order", f"{order_by or '(SELECT NULL)'} {order.value}")
        query = query.replace(":_limit", str(limit))

        return query