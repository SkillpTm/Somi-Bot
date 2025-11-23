import aiomysql # type: ignore
import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Database as sql
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot



class Database(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.sudo.subcommand(
        Commands().data["sudo database"].alias,
        Commands().data["sudo database"].description,
        name_localizations = {country_tag: Commands().data["sudo database"].name for country_tag in nextcord.Locale},
    )
    @nextcord_AC.check(Get.interaction_by_owner()) # type: ignore
    async def database(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        table: str = nextcord.SlashOption(
            Commands().data["sudo database"].parameters["table"].name,
            Commands().data["sudo database"].parameters["table"].description,
            required = True,
            choices = [
                db.CustomCommand._.get_table(), db.Feedback._.get_table(), db.HiddenChannel._.get_table(), db.Keyword._.get_table(),
                db.Level._.get_table(), db.LevelIgnoreChannel._.get_table(), db.LevelRole._.get_table(), db.Reminder._.get_table(),
                db.Server._.get_table(), db.Statistic._.get_table(), db.Telemetry._.get_table(), db.User._.get_table()
            ]
        ),
        where_query: str = nextcord.SlashOption(
            Commands().data["sudo database"].parameters["where_query"].name,
            Commands().data["sudo database"].parameters["where_query"].description,
            required = False,
            default = ""
        ),
        order_by: str = nextcord.SlashOption(
            Commands().data["sudo database"].parameters["order_by"].name,
            Commands().data["sudo database"].parameters["order_by"].description,
            required = False,
            default = ""
        ),
        order: str = nextcord.SlashOption(
            Commands().data["sudo database"].parameters["order"].name,
            Commands().data["sudo database"].parameters["order"].description,
            required = False,
            choices = ["ASC", "DESC"],
            default = ""
        )
    ) -> None:
        """This command reloads the bot, it can only be executed from the owner"""

        where_query, order_by = where_query.lower(), order_by.lower()

        await interaction.response.defer(ephemeral=True, with_message=True)

        async with sql()._pool.acquire() as con: # type: ignore
            async with con.cursor() as cur:
                await cur.execute(f"SELECT * FROM {table} LIMIT 1")
                result = await cur.fetchone()
                if result:
                    allowed_columns: list[str] = list(result.keys())
                else:
                    await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"```Table '{table}' is empty```"))
                    return

            await con.commit()

        query = f"SELECT * FROM {table} "
        parameters: list[str] = []

        if where_query:
            query += "WHERE "
            for index, pair in enumerate(temp_params := where_query.split(",")):
                key, value = pair.split("=", 1) if "=" in pair else ("", "")

                if not key.strip() in allowed_columns:
                    await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"```Column '{key.strip()}' does not exist in table '{table}'```"))
                    return

                query += f"`{key.strip()}` = %s "
                if index < len(temp_params) - 1:
                    query += "AND "

                parameters.append(value.strip())

        if (not order_by and order) or (order_by and not order):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("```Both 'order' and 'order-by' must be provided```"))
            return

        if order_by and order_by not in allowed_columns:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"```Column '{order_by}' does not exist in table '{table}'```"))
            return

        if order_by and order and order in ["ASC", "DESC"]:
            query += f"ORDER BY `{order_by}` {order}"

        output = ""
        con: aiomysql.Connection
        cur: aiomysql.Cursor
        row: dict[str, str | int | None]

        async with sql()._pool.acquire() as con: # type: ignore
            await con.autocommit(True)
            async with con.cursor() as cur:
                await cur.execute(query, tuple(parameters))
                async for row in cur:
                    if not output:
                        output += " | ".join(row.keys()) + "\n"
                        output += f"{'-' * 50}\n"

                    output += " | ".join(str(val) for val in row.values()) + "\n"

        if not output:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("```Empty set```"))
            return

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"```{output}```"[4096]))



def setup(client: SomiBot) -> None:
    client.add_cog(Database(client))