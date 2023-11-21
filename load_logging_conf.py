import logging.config
import logging
import yaml


def configure_logging():
    with open('logging.yaml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
