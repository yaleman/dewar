""" default ingestor. single threaded, kinda lazy. """

import hashlib
import time
from loguru import logger

import config

def hash_file(filename):
    with open(filename, 'rb') as fh:
        sha_sum = hashlib.sha256()
        # read a chunk
        while True:
            data = fh.read(HASH_BLOCK_SIZE)
            if not data:
                break
            sha_sum.update(data)
    return sha_sum.hexdigest()


class Ingestor():
    """ ingestor class """
    def __init__(self, 
            bucket: str,
            **kwargs,
            ):
        """ ingestor class """
        self.storage_backend = storage_backend

        self.bucket = bucket

        # the number of seconds between running the ingestion loop
        self.loop_delay = kwargs.get('loop_delay', 30)

    def ingest(self, filename: str, source_bucket: str):
        """ runs a single ingest cycle """
        logger.debug(f"Ingesting {filename} from {bucket}")
        

    def ingest_loop(self):
        """ runs an ingest cycle every self.loop_delay seconds """
        while True:
            self.ingest()
            logger.debug("Sleeping for {self.loop_delay} seconds")
            time.sleep(self.loop_delay)
