#!/usr/bin/env python
"""watch_url."""
import logging
import sys
from os.path import join
# from nameko.runners import ServiceRunner
# from nameko.testing.utils import get_container

try:
    import agents_common
except ImportError:
    from settings import PROJECT_PATH, AGENTS_COMMON_PATH
    logging.debug('It seems agents_common is not installed, '
                  'trying to import it from %s.' % AGENTS_COMMON_PATH)
    sys.path.append(AGENTS_COMMON_PATH)
    try:
        import agents_common
    except ImportError as e:
        logging.error('Could not import agents_common.')
        raise e

from model_watch_page import WatchAgent
from settings import LOGGING
from settings import STORE_URL, STORE_CONFIG_DB, STORE_CONFIG_DOC, STORE_DB
from settings import FETCH_PAGE_URL
from settings_agent import AGENT_TYPE, PAGE_TYPE, AGENT_ATTRIBUTE

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)
print 'LOG LEVEL watch_pages...'
print logging.getLevelName(logger.getEffectiveLevel())


def main():
    # config_dict = get_config_yaml(CONFIG_YAML_PATH)
    # c = update_config_yaml(config_dict, CONFIG_YAML_PATH)
    # runner = ServiceRunner(c)
    # runner.add_service(WatchURLService)
    # # container_a = get_container(runner, WatchURLService)
    # runner.start()
    # try:
    #     runner.wait()
    # except KeyboardInterrupt:
    #     runner.kill()
    # runner.stop()
    # # sys.exit()
    logger.info('Starting service...')
    watch = WatchAgent(STORE_URL, STORE_DB, STORE_CONFIG_DB, STORE_CONFIG_DOC,
                       AGENT_TYPE, PAGE_TYPE, AGENT_ATTRIBUTE, FETCH_PAGE_URL)
    watch.process_rules()

if __name__ == '__main__':
    main()
