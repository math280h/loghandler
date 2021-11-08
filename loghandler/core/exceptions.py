from datetime import datetime


class SendException(Exception):
    """Exception for sending logs."""

    def __init__(self, module: str, message: Exception, level: str = "ERROR") -> None:
        """Initialize Exception."""
        self.module = module
        self.message = message
        self.level = level

        super().__init__(self.message)


class ConfigurationException(Exception):
    """Exception for configuration errors."""

    def __init__(self, module: str, message: str) -> None:
        """Initialize Exception."""
        self.module = module
        self.message = message

        super().__init__(self.message)

    def __str__(self) -> str:
        """Define output for Configuration Exception."""
        return f"[{datetime.utcnow().strftime('%H:%M:%S')}][{self.module}][Invalid Configuration] {self.message}"
