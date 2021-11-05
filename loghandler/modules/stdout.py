from datetime import datetime
from typing import Any

from rich.columns import Columns
from rich.console import Console

from loghandler.core.helpers import get_level_name_from_value


class STDOUT:
    """
    STDOUT Log Handler.

    :param config: LogHandlerConfig object
    """

    def __init__(self, config: dict) -> None:
        """Initialize STDOUT Log Handler."""
        self.config = config
        self.console = Console()

    def handle(self, exception: Exception, stack: Any) -> None:
        """
        Handle logging of message.

        :param exception: Exception object
        :param stack: Call stack
        """
        filename = stack.filename.split("/")[-1]
        if len(filename) == len(stack.filename):
            filename = filename = stack.filename.split("\\")[-1]

        origin = f"{filename}:{stack.lineno}"
        now = datetime.now()

        output = [
            f"[{now.strftime('%H:%M:%S')}]\\[{origin}][{get_level_name_from_value(self.config['log_level'])}]:",
            f"{exception}",
        ]

        self.console.print(Columns(output))
