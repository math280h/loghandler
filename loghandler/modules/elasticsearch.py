from datetime import datetime
from socket import gethostname
from typing import Any

from elasticsearch import Elasticsearch

from loghandler.core.exceptions import ConfigurationException, SendException


class ElasticSearch:
    """
    ElasticSearch Log Handler.

    :param config: LogHandlerConfig object
    """

    def __init__(self, config: dict, es_config: dict) -> None:
        """Initialize ElasticSearch Log Handler."""
        self.config = config
        self.es_config = es_config

        if "hosts" not in self.es_config or type(self.es_config["hosts"]) is not list:
            raise ConfigurationException(
                "elasticsearch", "hosts must be specified and a list"
            )

        if "index" not in self.es_config or type(self.es_config["index"]) is not str:
            raise ConfigurationException(
                "elasticsearch", "index must be specified and a str"
            )

        if "ssl" not in self.es_config or type(self.es_config["ssl"]) is not bool:
            raise ConfigurationException(
                "elasticsearch", "ssl must be specified and a bool"
            )

        if (
            "verify_certs" not in self.es_config
            or type(self.es_config["verify_certs"]) is not bool
        ):
            raise ConfigurationException(
                "elasticsearch", "verify_certs must be specified and a bool"
            )

        if (
            "api_key" not in self.es_config
            or type(self.es_config["api_key"]) is not tuple
        ):
            raise ConfigurationException(
                "elasticsearch", "api_key must be specified and a tuple"
            )

        self.elasticsearch = Elasticsearch(
            hosts=es_config["hosts"],
            use_ssl=es_config["ssl"],
            verify_certs=es_config["verify_certs"],
            api_key=es_config["api_key"],
        )

        self.elasticsearch.indices.create(index=self.es_config["index"], ignore=400)

    def handle(self, level: str, exception: Exception, stack: Any) -> None:
        """
        Handle logging of message.

        :param level: Log level
        :param exception: Exception object
        :param stack: Call stack
        """
        try:
            self.elasticsearch.index(
                index=self.es_config["index"],
                document={
                    "timestamp": datetime.utcnow(),
                    "level": level.upper(),
                    "hostname": gethostname(),
                    "message": str(exception),
                    "occurred_at": {
                        "path": stack.filename.replace("\\", "/"),
                        "line": stack.lineno,
                    },
                },
            )
        except Exception as e:
            raise SendException("elasticsearch", e) from e
