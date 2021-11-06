# loghandler

![Lint](https://github.com/math280h/loghandler/actions/workflows/type-lint.yml/badge.svg)
![Downloads/month](https://img.shields.io/pypi/dm/loghandler)
![Bug reports](https://img.shields.io/github/issues-search/math280h/loghandler?label=Open%20bug%20reports&query=label%3Abug)

Easy logging package for all your logging needs.

## Features

- Log to multiple endpoints at once
- Support for STDOUT, Elasticsearch, and more coming soon.
- Easy syntax

## Installing

Install loghandler via pip
```shell
pip install loghandler
```

## Using

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

## Endpoints

The following endpoints are currently in the works and will be supported soon.

* database (MySQL, PostgreSQL, SQLite, ...)
* logstash
* sentry

### General Configuration

All endpoints accept a few global settings. They are shown below.

`log_level`: For the output it's applied to, this will overrule the global configuration level

### STDOUT

To use STDOUT as a log endpoint, add the following to your outputs array.
````python
{
    "type": "STDOUT"
}
````

### Elasticsearch

To use elasticsearch as a log endpoint, add the following to your outputs array.
````python
{
    "type": "elasticsearch", 
    "config": {
        "hosts": ["https://your-es-host.com:9243"],
        "ssl": True,
        "verify_certs": True,
        "index": "your-index",  # Index will be created if it doesn't exist
        "api_key": ("your-api-key-id", "your-api-key-secret")
    }
}
````

Next time something is logged you should see something like the following under your index:
````json
{
  "_index" : "logs",
  "_type" : "_doc",
  "_id" : "some-id",
  "_score" : 1.0,
  "_source" : {
    "timestamp" : "2021-11-05T04:16:25.250206",
    "level" : "DEBUG",
    "hostname" : "YOUR-HOSTNAME",
    "message" : "division by zero",
    "occurred_at" : {
      "path" : "/somepath/test.py",
      "line" : 22
    }
  }
}
````