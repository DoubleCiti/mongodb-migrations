import logging.config

logging.config.dictConfig(dict(
    version=1,
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.INFO,
            "stream": "ext://sys.stdout"
        }
    }
))
