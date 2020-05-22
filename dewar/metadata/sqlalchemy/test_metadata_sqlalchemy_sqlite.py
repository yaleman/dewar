""" terrible tests for the base metadata class """

import pytest
from loguru import logger

from .sqlalchemy_tests import test_get_hash, test_get_jobmeta, test_put_hash, test_put_jobmeta # pylint: disable=unused-import

@pytest.fixture(scope="session")
def connection_string(tmpdir_factory):
    """ returns a filename for a metadatastore object we can use and automagically clean up when tests are finished """
    filename = tmpdir_factory.mktemp("test").join("dewar.sqlite")
    logger.debug(f"Connection string: 'sqlite:///{filename}'")
    return f'sqlite:///{filename}'





# def test_put_othermeta(connection_string):
#     store = MetadataStore(filename=connection_string)
#     assert 1 == 2

# def test_get_othermeta(connection_string):
#     store = MetadataStore(filename=connection_string)
#     assert 1 == 2

# def test_get_othermeta_multiple_kwargs(connection_string):
#     # TODO: test multiple kwargs
#     assert True

# def test_del_othermeta(connection_string):
#     store = MetadataStore(filename=connection_string)
#     assert 1 == 2
