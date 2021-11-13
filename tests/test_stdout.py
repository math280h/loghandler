import signal
import unittest
import os
import sys
import subprocess

from loghandler import LogHandler
from loghandler.modules.stdout import STDOUT


class TestStdout(unittest.TestCase):
    """Test the STDOUT Module."""

    def test_init(self):
        """Test that the stdout module is correctly loaded."""
        logger = LogHandler({
            "log_level": "TRACE",
            "outputs": [
                {
                    "type": "stdout"
                }
            ]
        })

        assert "stdout" in logger.modules
        assert type(logger.modules["stdout"]) == STDOUT

    def test_output(self):
        """Test that stdout provides the correct output."""
        command = ["python", f"{os.path.dirname(os.path.abspath(__file__))}\\stdout.py"]

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        for line in iter(p.stdout.readline, b''):
            sys.stdout.flush()
            output = line.rstrip().decode().split("]:")[1]
            assert output == " This is working!"
            break

        p.send_signal(signal.SIGTERM)
