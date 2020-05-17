""" basic single threaded ingestor """

import tempfile
import time

from loguru import logger

import dewar.ingestor

class Ingestor(dewar.ingestor.Ingestor):
    """ single-threaded ingestor class """


    def ingest(self, **kwargs):
        """ runs a single ingest cycle
            pass it a bucket, it'll grab the first file it finds
                also pass the filename and it'll grab that file specifically.

            buckets in this case are the names of the stores in self.incoming
                which should be "known_good" or "other"
        """
        # find a thing to parse
        bucket, filename = self._find_file_to_ingest(**kwargs)
        if not bucket:
            return False
        logger.debug(f"Found a file to ingest: {bucket}/{filename}, getting it")

        filestore_object = self.incoming[bucket].get(filename)
        if not filestore_object:
            logger.error(f"Couldn't retrive {bucket}/{filename}")
            return False
        logger.debug(f"response keys: {filestore_object.keys()}")

        job = self.start_ingest_job(filename=filename, bucket=bucket)
        with tempfile.TemporaryFile(mode='w+b', buffering=8192, prefix="dewar_temparchive") as archive_tempfile:
            logger.debug(f"Temporary archive file path: {archive_tempfile}")
            # load the file from storage into the temporary file
            archive_tempfile.write(filestore_object.get('content'))

            # clear the write buffers and seek to 0 so we can read it back out
            archive_tempfile.flush()
            archive_tempfile.seek(0)

            with tempfile.TemporaryDirectory(prefix="dewar_ingestor") as tempdir:
                logger.debug(f"Archive extraction tempdir: {tempdir}")
                if filename.endswith(('.gz', '.bz2', 'lzma')):
                    logger.debug('tarfile to handle')
                    self._extract_tarfile_format(job=job, filehandle=archive_tempfile, tempdir=tempdir)
                else:
                    logger.error(f"No handler for {filename}")
        return True


    def ingest_loop(self):
        """ runs an ingest cycle every self.loop_delay seconds """
        while True:
            self.ingest()
            logger.debug("Sleeping for {self.loop_delay} seconds")
            time.sleep(self.loop_delay)
