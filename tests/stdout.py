from loghandler import LogHandler

logger = LogHandler({
    "log_level": "TRACE",
    "outputs": [
        {
            "type": "stdout"
        }
    ]
})

logger.log("DEBUG", Exception("This is working!"))
exit(0)
