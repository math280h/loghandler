# loghandler

loghandler allows you to easily log messages to multiple endpoints.

## Using

Install loghandler via pip
```shell
pip install loghandler
```

In your code import LogHandler and initalize it.
```python
from loghandler import LogHandler

logger = LogHandler({
    "log_level": "DEBUG",
    "outputs": [
        {
            "type": "STDOUT"
        }
    ]
})
```

You can now log messages to all your outputs via:
```python
logger.log('fatal', Exception("Something went HORRIBLY wrong"))
```

## Supported endpoints

* STDOUT

### Coming soon

* elasticsearch
* database (MySQL, PostgreSQL, SQLite, ...)
* logstash
* sentry

And probably more.
