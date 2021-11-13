import unittest

from elasticsearch import Elasticsearch

from loghandler import LogHandler
from loghandler.modules.elasticsearch import ElasticSearch


class TestElasticSearch(unittest.TestCase):
    """Test the ElasticSearch Module."""

    def test_init(self):
        """Test that the ElasticSearch module is correctly loaded."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "elasticsearch",
                    "config": {
                        "hosts": ["localhost:9200"],
                        "ssl": False,
                        "verify_certs": False,
                        "index": "logs",
                        "api_key": ("none", "none")
                    }
                }
            ]
        })

        assert "elasticsearch" in logger.modules
        assert type(logger.modules["elasticsearch"]) == ElasticSearch

    def test_output(self):
        """Test that ElasticSearch provides the correct output."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "elasticsearch",
                    "config": {
                        "hosts": ["localhost:9200"],
                        "ssl": False,
                        "verify_certs": False,
                        "index": "logs",
                        "api_key": ("none", "none")
                    }
                }
            ]
        })

        logger.log("DEBUG", Exception("This is working!"))

        es = Elasticsearch(
            hosts=["localhost:9200"],
            use_ssl=False,
            verify_certs=False,
            api_key=("none", "none"),
        )

        res = es.search(index="logs", query={"match_all": {}})['hits']['hits'][0]
        assert res["_source"]["message"] == "This is working!"
