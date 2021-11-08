from datetime import datetime
from typing import Any

from rich.columns import Columns
from rich.console import Console

from loghandler.core.exceptions import SendException


class STDOUT:
    """
    STDOUT Log Handler.

    :param config: LogHandlerConfig object
    """

    def __init__(self, config: dict) -> None:
        """Initialize STDOUT Log Handler."""
        self.config = config
        self.console = Console()

    def handle(self, level: str, exception: Exception, stack: Any) -> None:
        """
        Handle logging of message.

        :param level: Log level
        :param exception: Exception object
        :param stack: Call stack
        """
        try:
            now = datetime.now()

            if stack.filename != "Internal":
                filename = stack.filename.split("/")[-1]
                if len(filename) == len(stack.filename):
                    filename = filename = stack.filename.split("\\")[-1]

                origin = f"{filename}:{stack.lineno}"
                output = [
                    f"[{now.strftime('%H:%M:%S')}]\\[{origin}][{level.upper()}]:",
                    f"{exception}",
                ]
            else:
                output = [
                    f"[{now.strftime('%H:%M:%S')}]\\[loghandler][{level.upper()}]:",
                    f"{exception}",
                ]

            self.console.print(Columns(output))
        except Exception as e:
            raise SendException("stdout", e) from e
