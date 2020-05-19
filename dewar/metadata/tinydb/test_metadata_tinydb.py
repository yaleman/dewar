""" terrible tests for the base metadata class """

import os
import time

import pytest

from dewar.metadata.tinydb import MetadataStore
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
def metadata_filename(tmpdir_factory):
    """ returns a filename for a metadatastore object we can use and automagically clean up when tests are finished """
    filename = tmpdir_factory.mktemp("test").join("metadata.json")
    MetadataStore(filename=filename)
    return filename


def test_put_hash(metadata_filename):
    """ test putting a hash in """
    store = MetadataStore(filename=metadata_filename)
    assert store.put_hash(filehash=TEST_HASH, known_good=TEST_KG)

def test_get_hash(metadata_filename):
    """ test getting the hash back """
    store = MetadataStore(filename=metadata_filename)
    data = store.get_hash(TEST_HASH)
    assert data == {
        'filehash' : TEST_HASH,
        'known_good' : TEST_KG,
    }

def test_put_jobmeta(metadata_filename):
    """ tests inserting job metadata """
    store = MetadataStore(filename=metadata_filename)

    assert store.put_metadata(metadata_type='job', **TEST_JOB_METADATA)

def test_get_jobmeta(metadata_filename):
    """ tests pulling back the job metadata inserted in test_put_jobmeta """
    store = MetadataStore(filename=metadata_filename)
    result = store.get_metadata(metadata_type='job', guid=TEST_JOB_METADATA['guid'])
    assert result == [TEST_JOB_METADATA]


# def test_put_othermeta(metadata_filename):
#     store = MetadataStore(filename=metadata_filename)
#     assert 1 == 2

# def test_get_othermeta(metadata_filename):
#     store = MetadataStore(filename=metadata_filename)
#     assert 1 == 2

# def test_get_othermeta_multiple_kwargs(metadata_filename):
#     # TODO: test multiple kwargs
#     assert True

# def test_del_othermeta(metadata_filename):
#     store = MetadataStore(filename=metadata_filename)
#     assert 1 == 2

