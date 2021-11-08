from dataclasses import dataclass


@dataclass
class InternalStack:
    """Internal Stack."""

    filename: str = "Internal"
    lineno: str = "Internal"


def get_level_value(level: str) -> int:
    """
    Get the level value of a log level.

    :param level: The log level.
    :return: The level value.
    """
    level = level.upper()

    if level == "TRACE":
        return 1
    elif level == "DEBUG":
        return 10
    elif level == "INFO":
        return 20
    elif level == "WARNING":
        return 30
    elif level == "ERROR":
        return 40
    elif level == "FATAL":
        return 50
    else:
        raise ValueError("Invalid log level")


def get_level_name_from_value(level: int) -> str:
    """
    Get the level name of a log level.

    :param level: The log level.
    :return: The level name.
    """
    if level == 1:
        return "TRACE"
    elif level == 10:
        return "DEBUG"
    elif level == 20:
        return "INFO"
    elif level == 30:
        return "WARNING"
    elif level == 40:
        return "ERROR"
    elif level == 50:
        return "FATAL"
    else:
        raise ValueError("Invalid log level")
