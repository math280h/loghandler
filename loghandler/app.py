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
            raise ValueError("`outputs` must contain at least one ouput")

        self.config["log_level"] = get_level_value(self.config["log_level"])

        self.modules = {}
        for handler in self.config["outputs"]:
            if "type" not in handler:
                raise ValueError("`type` is a required parameter for outputs")
            if handler["type"] == "stdout":
                imp = importlib.import_module("loghandler.modules.stdout")
                self.modules["stdout"] = getattr(imp, "STDOUT")(self.config)

    def log(self, level: str, exception: Exception) -> None:
        """
        Log a message.

        :param level: The level of the message.
        :param exception: The exception to log.
        """
        log_level = get_level_value(level)

        if log_level < self.config["log_level"]:
            return

        for _, module in self.modules.items():
            stack = inspect.stack()[1]
            module.handle(exception, stack)