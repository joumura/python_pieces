import os
import logging

CONFIG_FILEPATH = os.path.dirname(os.path.abspath(__file__)) + '/logging.ini'
if os.path.isfile(CONFIG_FILEPATH):
    import logging.config
    logging.config.fileConfig(CONFIG_FILEPATH)
else:
    logging.basicConfig(
        level=logging.DEBUG, datefmt='%H:%M:%S',
        format="%(asctime)s %(levelname)-7s %(name)s:%(lineno)d - %(message)s")

logger = logging.getLogger(__name__)


def main():
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    try:
        raise Exception('no problem')
    except Exception:
        logger.exception('catch')
        raise


if __name__ == '__main__':
    main()
