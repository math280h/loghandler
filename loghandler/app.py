import importlib
import inspect

from loghandler.core.helpers import get_level_value


class LogHandler:
    """
    LogHandler class is the main class of the loghandler package.

    :param config: The configuration object.
    """

    def __init__(self, config: dict) -> None:
        """Initialize LogHandler."""
        self.config = config

        if "log_level" not in self.config:
            raise ValueError("`log_level` is a required parameter")

        if "outputs" not in self.config:
            raise ValueError("`outputs` is a required parameter")

        if not self.config["outputs"]:
            raise ValueError("`outputs` must contain at least one output")

        self.config["log_level"] = get_level_value(self.config["log_level"])

        self.modules = {}
        for handler in self.config["outputs"]:
            if "type" not in handler:
                raise ValueError("`type` is a required parameter for outputs")

            if handler["type"].lower() == "stdout":
                imp = importlib.import_module("loghandler.modules.stdout")
                self.modules["stdout"] = getattr(imp, "STDOUT")(self.config)
            elif handler["type"].lower() == "elasticsearch":
                imp = importlib.import_module("loghandler.modules.elasticsearch")
                if "config" not in handler:
                    raise ValueError(
                        "`config` is a required parameter for elasticsearch"
                    )
                self.modules["elasticsearch"] = getattr(imp, "ElasticSearch")(
                    self.config, handler["config"]
                )
            elif (
                handler["type"].lower() == "sqlite"
                or handler["type"].lower() == "mysql"
                or handler["type"].lower() == "pgsql"
            ):
                imp = importlib.import_module("loghandler.modules.database")
                if "config" not in handler:
                    raise ValueError(
                        f"`config` is a required parameter for {handler['type'].lower()}"
                    )
                self.modules[handler["type"].lower()] = getattr(imp, "Database")(
                    self.config, handler["config"], handler["type"].lower()
                )

    def log(self, level: str, exception: Exception) -> None:
        """
        Log a message.

        :param level: The level of the message.
        :param exception: The exception to log.
        """
        log_level = get_level_value(level)

        for key, module in self.modules.items():
            output = [
                output for output in self.config["outputs"] if output["type"] == key
            ][0]

            if "log_level" in output:
                if log_level < get_level_value(output["log_level"]):
                    continue
            elif log_level < self.config["log_level"]:
                continue

            stack = inspect.stack()[1]
            module.handle(level.lower(), exception, stack)
