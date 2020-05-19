""" default ingestor. single threaded, kinda lazy. """

import os
import tarfile
import tempfile
import time

from loguru import logger

import config
from dewar.utilities import hash_file, generate_job_id

class Ingestor():
    """ Parent Ingestor class, should not be used directly.
        Provides common functions for extension.
    """
    def __init__(self,
                 **kwargs,
                 ):
        """ ingestor class """
        #self.storage_backend = storage_backend
        self.metadatastore = config.MetadataStore
        # the number of seconds between running the ingestion loop
        self.loop_delay = kwargs.get('loop_delay', 30)
        self.incoming = {}

    def ingest(self, **kwargs):
        """ runs a single ingest cycle
            pass it a bucket, it'll grab the first file it finds
                also pass the filename and it'll grab that file specifically.

            buckets in this case are the names of the stores in self.incoming
                which should be "known_good" or "other"
        """
        raise NotImplementedError

    def ingest_loop(self):
        """ runs an ingest cycle every self.loop_delay seconds """
        raise NotImplementedError

    def start_ingest_job(self, **kwargs):
        """ create and store an ingest job, should use all the standard functions """

        # generate and store the metadata for this job
        timestamp = time.time()

        jobdata = {
            'id' : generate_job_id(),
            'timestamp' : kwargs.get('timestamp', timestamp),
            'name' : kwargs.get('filename', kwargs.get('name', f'unnamed-{timestamp}')),
            'source_bucket' : kwargs.get('bucket', None),
            'known_good' : kwargs.get('known_good', False)
        }
        if kwargs.get('bucket') == "known_good":
            jobdata['known_good'] = True

        logger.debug(jobdata)

        # TODO: store the job metadata
        self.metadatastore.put(metadata_type='job', **jobdata)
        return jobdata

    def _find_file_to_ingest(self, **kwargs):
        """ find a file to deal with
            possible arguments: filename and or storage

            if you set storage, it'll just grab the first thing it finds
                in the storage backend self.incoming[storage]
            if you also set filename, it'll pull that filename from that storage

            if you don't set a storage it'll try them in the following order:
                - known_good
                - other
        """
        # which mode are we running in
        if 'filename' in kwargs and 'storage' not in kwargs: #pylint: disable=no-else-raise
            raise ValueError("Need a storage backend name if you specify filename")

        if 'filename' in kwargs and 'storage' in kwargs:
            # we're looking for a particular thing
            filename = kwargs.get('filename')
            bucket = kwargs.get('storage')
            # TODO: grab a file
        elif 'filename' not in kwargs and 'storage' in kwargs:
            bucket = kwargs.get('storage')
            # we're just grabbing the first thing in the storage
            if bucket not in self.incoming:
                raise ValueError(f"storage backend {bucket} not found")
            files = self.incoming[bucket].dir()
            if not files:
                return False

            logger.debug(f"File list: {files}")
            filename = list(files.keys())[0]
            foundfile = True

        else:
            foundfile = False
            for bucket in ('known_good', 'other'):
                if bucket in self.incoming:
                    # get first file from bucket
                    files = self.incoming[bucket].dir()
                    if files:
                        logger.debug(f"Files: {files}")
                        filename = list(files.keys())[0]
                        foundfile = True
                        break
        if not foundfile:
            return False, False
        return bucket, filename

    # file-type handlers
    def _store_dir(self, job, tempdir, archive, member, **kwargs):
        """ this should handle storing metadata for directories """
        logger.warning(f"_store_link is not actually implemented: {self} {tempdir} {archive} {kwargs} {member} {job}")

    def _store_file(self, job, tempdir, archive, member, **kwargs):
        """ this should handle storing files """
        logger.warning(f"_store_file is not actually implemented: {self} {tempdir} {archive} {kwargs} {member} {job}")
        filename = f"{tempdir}/{member.name}"
        filesize = os.stat(filename).st_size
        filehash = hash_file(filename)
        logger.debug(f"File size of member in tempdir: {filesize}")
        logger.debug(f"File hash of {filename}: {filehash}")
        filedata = {
            'filehash' : filehash,
            'size' : filesize,
            'known_good' : job.known_good,
        }

        logger.debug("checking for existing file hash")
        hashcheck = self.metadatastore.get_or_insert('file', **filedata)
        if hashcheck:
            logger.debug("metadata already stored")
            logger.debug("storing metadata")

    def _store_symlink(self, job, tempdir, archive, member, **kwargs):
        """ this should handle storing metadata for symlink - I'm guessing we shouldn't try to read this as a file? """
        logger.warning(f"_store_link is not actually implemented: {self} {tempdir} {archive} {kwargs} {member} {job}")

    # archive type handlers
    def _extract_tarfile_format(self, job, filehandle, tempdir):
        """ pass it a filehandle-like thing and you'll get back a location where we've extracted all the files """

        logger.debug("Opening tarfile... we have {tempdir} to work in")
        archive = tarfile.open(mode='r', fileobj=filehandle, bufsize=8192)
        # TODO: decide if this is risky or not?
        #logger.debug(archive.extractall(tempdir))
        for member in archive.getmembers():
            logger.debug(member.name)
            handler = None
            if member.isfile():
                handler = self._store_file
            elif member.isdir():
                handler = self._store_dir
            elif member.issym() or member.islink():
                handler = self._store_symlink
            else:
                logger.error(f"We don't have a handler for this... {member}")
            if handler:
                archive.extract(member, tempdir, set_attrs=False)

                handler(job, tempdir, archive, member)
