from datetime import datetime, timedelta
import importlib
import inspect

from loghandler.core.exceptions import SendException
from loghandler.core.helpers import get_level_value, InternalStack


class LogHandler:
    """
    LogHandler class is the main class of the loghandler package.

    :param config: The configuration object.
    """

    def __init__(self, config: dict) -> None:
        """Initialize LogHandler."""
        self.config = config
        self.failing_outputs: dict = {}

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
                try:
                    imp = importlib.import_module("loghandler.modules.stdout")
                    self.modules["stdout"] = getattr(imp, "STDOUT")(self.config)
                except Exception as e:
                    print(e)
            elif handler["type"].lower() == "elasticsearch":
                try:
                    imp = importlib.import_module("loghandler.modules.elasticsearch")
                    if "config" not in handler:
                        raise ValueError(
                            "`config` is a required parameter for elasticsearch"
                        )
                    self.modules["elasticsearch"] = getattr(imp, "ElasticSearch")(
                        self.config, handler["config"]
                    )
                except Exception as e:
                    print(e)
            elif (
                handler["type"].lower() == "sqlite"
                or handler["type"].lower() == "mysql"
                or handler["type"].lower() == "pgsql"
            ):
                try:
                    imp = importlib.import_module("loghandler.modules.database")
                    if "config" not in handler:
                        raise ValueError(
                            f"`config` is a required parameter for {handler['type'].lower()}"
                        )
                    self.modules[handler["type"].lower()] = getattr(imp, "Database")(
                        self.config, handler["config"], handler["type"].lower()
                    )
                except Exception as e:
                    print(e)
                    exit(1)

    def log(
        self,
        level: str,
        exception: Exception,
        skip_module: list = None,
        internal: bool = False,
    ) -> None:
        """
        Log a message.

        :param level: The level of the message.
        :param exception: The exception to log.
        :param skip_module: This parameter allows you to skip specific modules for logging.
        :param internal: This parameter indicates if the log came from loghandler itself.
        """
        log_level = get_level_value(level)

        for key, module in self.modules.items():
            if skip_module is not None and type(skip_module) is list:
                is_module = False
                for sm in skip_module:
                    if sm == key:
                        is_module = True

                if is_module:
                    continue

            output = [
                output for output in self.config["outputs"] if output["type"] == key
            ][0]

            if "log_level" in output:
                if log_level < get_level_value(output["log_level"]):
                    continue
            elif log_level < self.config["log_level"]:
                continue

            stack = inspect.stack()[1] if not internal else InternalStack()
            try:
                if (
                    output["type"] in self.failing_outputs
                    and self.failing_outputs[output["type"]] is not None
                ):
                    retry_after = (
                        int(output["retry_after"]) if "retry_after" in output else 15
                    )
                    if (
                        self.failing_outputs[output["type"]]["failure_timestamp"]
                        + timedelta(seconds=retry_after)
                        > datetime.utcnow()
                    ):
                        continue
                module.handle(level.lower(), exception, stack)
                self.failing_outputs[output["type"]] = None

            except SendException as e:
                if "report_error" in output and output["report_error"] is False:
                    continue
                else:
                    self.log(e.level, e, [e.module], internal=True)
                    self.failing_outputs[e.module] = {
                        "failure_timestamp": datetime.utcnow(),
                    }
            except Exception as e:
                if "report_error" in output and output["report_error"] is False:
                    continue
                else:
                    self.log("ERROR", e, [output["type"]], internal=True)
                    self.failing_outputs[output["type"]] = {
                        "failure_timestamp": datetime.utcnow(),
                    }
