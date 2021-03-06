#!/usr/bin/env python3

""" run some basic tests on the s3 storage thing """

import os

from loguru import logger

from dewar.metadata import MetadataStore
from dewar.storage.s3 import Storage

# not actually unused - config sets environment variables
import config #pylint: disable=unused-import

TESTBUCKET = 'test-dewar'

STORAGE = Storage(bucket=TESTBUCKET,
                  endpoint_url=os.environ.get('S3_ENDPOINT_URL'),
                  metadatastore=MetadataStore,
                  )


def test_put(storage_object=STORAGE):
    """ tests putting README.md into the test bucket """
    with open('README.md', 'r') as filehandle:
        assert storage_object.put("README.md",
                                  contents=filehandle.read(),
                                  metadata={},
                                  )


def test_dir(storage_object=STORAGE):
    """ tests storage.s3.dir """
    logger.info("This should return a list of files...")
    files = storage_object.dir()
    for filename in files:
        logger.debug(f"{filename} {files[filename]}")
    assert files

def test_get(storage_object=STORAGE):
    """ tests getting README.md back """
    result = storage_object.get('README.md')
    file_size = os.stat('README.md').st_size

    assert result.get('size') == file_size

def test_delete(storage_object=STORAGE):
    """ tests deleting README.md """
    assert storage_object.delete("README.md")

if __name__ == '__main__':
    logger.debug(f"Environment variables: {os.environ}")
