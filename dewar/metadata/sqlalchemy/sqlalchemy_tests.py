
import time
import pytest

from loguru import logger


from dewar.utilities import generate_job_id

from dewar.metadata.sqlalchemy import MetadataStore

TEST_HASH = '49db13a8c10399aa525df992a14788c827e18371205fb086a1e0d262f5b4beba' # sha256 of README.md at some rando point
TEST_KG = True


TEST_JOB_METADATA = { # ingestion job
        'guid' : generate_job_id(), # a dewar.utilities.get_job_id() is a uuid.uuid4, but ... standard.
        'timestamp' : int(time.time()),  # unix seconds since epoch
        'name' : "2020-05-20-examplefile.tar.gz", # filename of the archive ingested
        'notes' : "These are some funky notes, don't you know? ÷",
        'known_good' : True, # if the whole job was tagged known-good
    }

def test_put_hash(connection_string): # pylint: disable=redefined-outer-name
    """ test putting a hash in """
    store = MetadataStore(connection_string=connection_string)
    assert store.put_hash(filehash=TEST_HASH, known_good=TEST_KG, size=123)

def test_get_hash(connection_string): # pylint: disable=redefined-outer-name
    """ test getting the hash back """
    store = MetadataStore(connection_string=connection_string)
    data = store.get_hash(TEST_HASH)
    logger.debug(data)
    logger.debug(dir(data))
    assert data == {
        'filehash' : TEST_HASH,
        'known_good' : TEST_KG,
        'size' : 123,
        'filetype' : None,
    }

def test_put_jobmeta(connection_string): # pylint: disable=redefined-outer-name
    """ tests inserting job metadata """
    store = MetadataStore(connection_string=connection_string)

    assert store.put(metadata_type='job', **TEST_JOB_METADATA)

def test_get_jobmeta(connection_string): # pylint: disable=redefined-outer-name
    """ tests pulling back the job metadata inserted in test_put_jobmeta """
    store = MetadataStore(connection_string=connection_string)
    result = store.get(metadata_type='job', guid=TEST_JOB_METADATA['guid'])
    assert result == [TEST_JOB_METADATA]