""" terrible tests for the base metadata class """

import time
from loguru import logger
import pytest

from dewar.metadata.sqlalchemy import MetadataStore
from dewar.utilities import generate_job_id

TEST_HASH = '49db13a8c10399aa525df992a14788c827e18371205fb086a1e0d262f5b4beba' # sha256 of README.md at some rando point
TEST_KG = True

TEST_JOB_METADATA = { # ingestion job
        'guid' : generate_job_id(), # a dewar.utilities.get_job_id() is a uuid.uuid4, but ... standard.
        'timestamp' : int(time.time()),  # unix seconds since epoch
        'name' : "2020-05-20-examplefile.tar.gz", # filename of the archive ingested
        'notes' : "These are some funky notes, don't you know? ÷",
        'known_good' : True, # if the whole job was tagged known-good
    }

@pytest.fixture(scope="session")
def connection_string(tmpdir_factory):
    """ returns a filename for a metadatastore object we can use and automagically clean up when tests are finished """
    connection_string = "postgresql://postgres@database/test"
    logger.debug(f"Connection string: '{connection_string}")
    return connection_string

from .sqlalchemy_tests import test_get_hash, test_get_jobmeta, test_put_hash, test_put_jobmeta
