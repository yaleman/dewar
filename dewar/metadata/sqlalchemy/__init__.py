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
from ...constants import METADATA_TYPES


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
        self.session.add(newfile)
        self.session.commit()
        return True

    def get_hash(self, filehash: str):
        """ sqlalchemy implementation
            args: filehash
        """
        result = self.session.query(File).filter(File.filehash == filehash)
        if not result:
            return False
        data = result.one()
        return {
            'filehash' : data.filehash,
            'size' : data.size,
            'known_good' : data.known_good,
            'filetype' : data.filetype,
        }


    def put(self, metadata_type, **kwargs):
        """ generic metadata inserter - only required thing is type
            to delineate from other fields - as it is the table name """
        if metadata_type == 'job':
            newobject = Job(**kwargs)
        elif metadata_type == 'jobfile':
            newobject = JobFile(**kwargs)
            # TODO: test jobfile in test_metadata_sqlalchemy_sqlite.py:put_metadata
        else:
            raise ValueError(f"Can't handle metadata_type {metadata_type} right now")
        self.session.add(newobject)
        self.session.commit()
        return True

    def get(self, metadata_type, **kwargs):
        """ generic metadata getter
            only required thing is metadata_type to delineate from other fields - as it is the table name

            kwargs should be search terms, beware this is likely a terrible implementation
            """
        if metadata_type == 'job':
            result = self.session.query(Job).filter_by(**kwargs)
        elif metadata_type == 'jobfile':
            result = self.session.query(JobFile).filter_by(**kwargs)
            # TODO: test jobfile in test_metadata_sqlalchemy_sqlite.py:get_metadata
        else:
            raise ValueError(f"Can't handle metadata_type {metadata_type} right now")
        if not result:
            return False
        logger.debug(result)


        return clean_data_cols(metadata_type, result)
    # TODO: dewar.metadata.del_hash() ?

def clean_data_cols(metadata_type, result):
    """ cleans up or warns about columns in query responses that should not be there """
    data = [row.__dict__ for row in result.all()]
    for row in data:
        if metadata_type != 'other':
            for col in row:
                if col not in METADATA_TYPES[metadata_type]:
                    logger.debug(f"unexpected column in response from storage: {col}")
        if row.get('_sa_instance_state'):
            del row['_sa_instance_state']
    return data
