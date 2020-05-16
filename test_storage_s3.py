#!/usr/bin/env python3

""" run some basic tests on the s3 storage thing """

import os
from loguru import logger
from dewar.storage.s3 import Storage
from dewar.metadata import MetadataStore
import config

#config.AWS_SECRET_KEY_ID
STORAGE = Storage(bucket='test-dewar',
                  endpoint_url=config.s3_endpoint,
                  aws_access_key_id=config.AWS_SECRET_KEY_ID,
                  aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                  metadatastore=MetadataStore,
                  )


def test_dir(storage_object=STORAGE):
    """ tests storage.s3.dir """
    logger.info("This should return a list of files...")
    files = storage_object.dir('dewar-incoming-knowngood')
    for filename in files:
        logger.debug(f"{filename} {files[filename]}")
    assert files

def test_put(storage_object=STORAGE):
    """ tests putting README.md into the test bucket """
    with open('README.md', 'r') as filehandle:
        assert storage_object.put("README.md",
                                  contents=filehandle.read(),
                                  metadata={},
                                  )

def test_get(storage_object=STORAGE):
    """ tests getting README.md back """
    result = storage_object.get('README.md')
    file_size = os.stat('README.md').st_size

    assert result.get('size') == file_size

def test_delete(storage_object=STORAGE):
    """ tests deleting README.md """
    assert storage_object.delete("README.md")

