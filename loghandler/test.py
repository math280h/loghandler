import time

from loghandler.app import LogHandler

logger = LogHandler({"log_level": "DEBUG", "outputs": [{"type": "stdout"}]})

for _ in range(0, 10):
    logger.log("debug", Exception("Test"))
    time.sleep(0.5)
