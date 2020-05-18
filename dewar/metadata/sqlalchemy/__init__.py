""" sqlalchemy-based class for storage backend """
import os
import pathlib
import sys

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

import config
from .models import Base, File, Job, JobFile


class MetadataStore():
    """ base class for the metadata store """
    def __init__(self, **kwargs):
        self.table_prefix = kwargs.get('table_prefix', 'dewar_')
        self.connection_string = kwargs.get('connection_string', 'sqlite://dewar.sqlite')

        logger.debug(f"Attempting to open {self.connection_string}")
        try:
            self.engine = create_engine(self.connection_string)
            Base.metadata.create_all(self.engine)
            Base.metadata.bind = self.engine
            self.dbsession = sessionmaker(bind=self.engine)
            self.session = self.dbsession()
        except OperationalError as error_message:
            quit_message = f"OperationalError opening database: {error_message}"
            logger.error(quit_message)
            sys.exit(quit_message)

    def put_hash(self, filehash: str, **kwargs):
        """ sqlalchemy implementation
            args: filehash, str
        """
        newfile = File(
            filehash=filehash,
            size=kwargs.get('size', -1),
            filetype=kwargs.get('filetype', None),
            known_good=kwargs.get('known_good', False),
        )
        self.session.add(newfile) #pylint: disable=no-member
        self.session.commit() #pylint: disable=no-member
        return True

    def get_hash(self, filehash: str):
        """ sqlalchemy implementation
            args: filehash
        """
        result = self.session.query(File).filter(File.filehash == filehash) #pylint: disable=no-member
        if not result:
            return False
        data = result.one()
        return {
            'filehash' : data.filehash,
            'size' : data.size,
            'known_good' : data.known_good,
            'filetype' : data.filetype,
        }


    def put_metadata(self, metadata_type, **kwargs):
        """ generic metadata inserter - only required thing is type
            to delineate from other fields - as it is the table name """
        raise NotImplementedError("This is the shell")

    def get_metadata(self, metadata_type, **kwargs):
        """ generic metadata getter
            only required thing is metadata_type to delineate from other fields - as it is the table name

            kwargs should be search terms, beware this is likely a terrible implementation
            """
        raise NotImplementedError("This is the shell")

    # TODO: dewar.metadata.del_hash() ?
