from socket import gethostname
from datetime import datetime
from typing import Any

from elasticsearch import Elasticsearch


class ElasticSearch:
    """
    ElasticSearch Log Handler.

    :param config: LogHandlerConfig object
    """

    def __init__(self, config: dict, es_config: dict) -> None:
        """Initialize ElasticSearch Log Handler."""
        self.config = config
        self.es_config = es_config

        self.elasticsearch = Elasticsearch(
            hosts=es_config["hosts"],
            use_ssl=es_config["ssl"],
            verify_certs=es_config["verify_certs"],
            api_key=es_config["api_key"]
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
                },
            )
        except Exception as e:
            print(e)
