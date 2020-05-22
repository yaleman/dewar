""" terrible tests for the base metadata class """

import pytest
from loguru import logger

from .sqlalchemy_tests import test_get_hash, test_get_jobmeta, test_put_hash, test_put_jobmeta # pylint: disable=unused-import

@pytest.fixture(scope="session")
def connection_string():
    """ returns a filename for a metadatastore object we can use and automagically clean up when tests are finished """
    retstr = "postgresql://postgres@postgres/test"
    logger.debug(f"Connection string: '{retstr}")
    return retstr
