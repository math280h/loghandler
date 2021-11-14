import unittest

from sqlalchemy import create_engine, text

from loghandler import LogHandler
from loghandler.modules.database import Database


class TestDatabase(unittest.TestCase):
    """Test the Database Module."""

    def test_init(self):
        """Test that the ElasticSearch module is correctly loaded."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "sqlite",
                    "config": {
                        "table_name": "logs",
                        "db_path": "/tmp/db.sqlite",
                    }
                },
                {
                    "type": "mysql",
                    "config": {
                        "table_name": "logs",
                        "connection_string": "root:password@localhost:3306/test"
                    }
                },
                {
                    "type": "pgsql",
                    "config": {
                        "table_name": "logs",
                        "connection_string": "test:password@localhost:5432/test"
                    }
                }
            ]
        })

        assert "sqlite" in logger.modules
        assert "mysql" in logger.modules
        assert "pgsql" in logger.modules
        assert type(logger.modules["sqlite"]) == Database
        assert type(logger.modules["mysql"]) == Database
        assert type(logger.modules["pgsql"]) == Database

    def test_sqlite_output(self):
        """Test that sqlite provides the correct output."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "sqlite",
                    "config": {
                        "table_name": "logs",
                        "db_path": "/tmp/db.sqlite",
                    }
                }
            ]
        })

        logger.log("DEBUG", Exception("This is working!"))

        engine = create_engine(
            f"sqlite+pysqlite:////tmp/db.sqlite",
            echo=False,
            future=True,
        )

        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM logs"))

            for item in result:
                assert item[1] == "This is working!"

    def test_mysql_output(self):
        """Test that mysql provides the correct output."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "mysql",
                    "config": {
                        "table_name": "logs",
                        "connection_string": "root:password@localhost:3306/test"
                    }
                }
            ]
        })

        logger.log("DEBUG", Exception("This is working!"))

        engine = create_engine(
            "mysql+pymysql://root:password@localhost:3306/test",
            echo=False,
            future=True,
        )

        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM logs"))

            for item in result:
                assert item[1] == "This is working!"

    def test_pgsql_output(self):
        """Test that pgsql provides the correct output."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "pgsql",
                    "config": {
                        "table_name": "logs",
                        "connection_string": "test:password@localhost:5432/test"
                    }
                }
            ]
        })

        logger.log("DEBUG", Exception("This is working!"))

        engine = create_engine(
            "postgresql://test:password@localhost:5432/test",
            echo=False,
            future=True,
        )

        with engine.begin() as conn:
            result = conn.execute(text("SELECT * FROM logs"))

            for item in result:
                assert item[1] == "This is working!"
