from datetime import datetime
from typing import Any

from rich.console import Console
from sqlalchemy import (
    Column,
    create_engine,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    text,
)

from loghandler.core.exceptions import ConfigurationException, SendException


class Database:
    """
    Database Log Handler.

    :param config: LogHandlerConfig object
    """

    def __init__(self, config: dict, db_config: dict, db_type: str) -> None:
        """Initialize Database Log Handler."""
        self.config = config
        self.console = Console()

        self.db_config = db_config
        self.db_type = db_type

        if "table_name" not in db_config or type(db_config["table_name"]) is not str:
            raise ConfigurationException(
                self.db_type, "database table_name must be specified and a str"
            )

        if db_type == "sqlite":
            if "db_path" not in db_config or type(db_config["db_path"]) is not str:
                raise ConfigurationException(
                    self.db_type, "db_path must be specified and a str"
                )

            self.engine = create_engine(
                f"sqlite+pysqlite:///{db_config['db_path']}", echo=False, future=True
            )
        elif db_type == "mysql" or db_type == "pgsql":
            if (
                "connection_string" not in db_config
                or type(db_config["connection_string"]) is not str
            ):
                raise ConfigurationException(
                    self.db_type, "connection_string must be specified and a str"
                )

            full_connection_string = (
                f"mysql+pymysql://{db_config['connection_string']}"
                if db_type == "mysql"
                else f"postgresql://{db_config['connection_string']}"
            )

            self.engine = create_engine(
                full_connection_string,
                echo=False,
                future=True,
            )
        metadata = MetaData()

        Table(
            db_config["table_name"],
            metadata,
            Column("id", Integer, primary_key=True),
            Column("message", Text),
            Column("level", String(7)),
            Column("origin", String(255)),
            Column("timestamp", DateTime),
        )

        metadata.create_all(self.engine)

    def handle(self, level: str, exception: Exception, stack: Any) -> None:
        """
        Handle logging of message.

        :param level: Log level
        :param exception: Exception object
        :param stack: Call stack
        """
        filename = stack.filename.replace("\\", "/")
        origin = f"{filename}:{stack.lineno}"
        now = datetime.now()

        try:
            with self.engine.begin() as conn:
                conn.execute(
                    text(
                        f"INSERT INTO {self.db_config['table_name']} (message, level, origin, timestamp) "
                        "VALUES (:message, :level, :origin, :timestamp)"
                    ),
                    [
                        {
                            "message": str(exception),
                            "level": level.upper(),
                            "origin": origin,
                            "timestamp": now,
                        }
                    ],
                )
        except Exception as e:
            raise SendException(self.db_type, e) from e
