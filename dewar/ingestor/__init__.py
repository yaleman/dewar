""" default ingestor. single threaded, kinda lazy. """

import time
from loguru import logger

import config
from dewar.utilities import hash_file



class Ingestor():
    """ ingestor class """
    def __init__(self,
                 **kwargs,
                 ):
        """ ingestor class """
        #self.storage_backend = storage_backend

        # the number of seconds between running the ingestion loop
        self.loop_delay = kwargs.get('loop_delay', 30)

    def ingest(self, **kwargs):
        """ runs a single ingest cycle

            possible arguments: filename and or bucket

            if you set bucket, it'll just grab the first thing it finds
            if you also set filename, it'll pull that filename from the bucket

            if you don't set a bucket it'll try them in the following order:
                - incoming-other
                - incoming-knowngood
        """

        # which mode are we running in
        if 'filename' in kwargs and 'bucket' not in kwargs: #pylint: disable=no-else-raise
            raise ValueError("Need a bucket if you specify filename")

        if 'filename' in kwargs and 'bucket' in kwargs:
            # we're looking for a particular thing
            filename = kwargs.get('filename')
            bucket = kwargs.get('bucket')
        elif 'filename' not in kwargs and 'bucket' in kwargs:
            # we're just grabbing the first thing in the bucket
            # TODO: work out how to handle storage backends
            #filename = storage_backend.dir(kwargs.get('bucket'))
            pass

        logger.debug(f"Shutting up pylint for now {filename} {bucket} loop delay {self.loop_delay}")

    def ingest_loop(self):
        """ runs an ingest cycle every self.loop_delay seconds """
        while True:
            self.ingest()
            logger.debug("Sleeping for {self.loop_delay} seconds")
            time.sleep(self.loop_delay)
