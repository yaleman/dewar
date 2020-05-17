""" base metadata store class, uses tinyDB """

from tinydb import TinyDB, Query
from loguru import logger

from ..constants import METADATA_TYPES



class MetadataStore():
    """ base class for the metadata store """
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename', False)
        if not self.filename:
            error_message = "Please set a filename for MetadataStore"
            logger.error(error_message)
            raise ValueError(error_message)
        
        self.tinydb = TinyDB(self.filename)

        # pre-create all the default tables
        self.dbtable = {}
        for table in METADATA_TYPES:
            self.dbtable[table] = self.tinydb.table(name=table)

    def get_hash(self, filehash: str):
        """ base implementation """
        result = self.dbtable['file'].search(Query().filehash==filehash)
        if not result: #pylint: disable=no-else-return
            return False
        elif len(result) > 1:
            raise ValueError(f"More than one result returned for filehash, that's bad? {result}")
        else:
            return result[0]
        

    def put_hash(self, filehash: str, **kwargs):
        """ base implementation """
        # TODO: dewar.metadata.put_hash: look to see if the hash already exists, and either update or warn if putting the same thing again

        filedata = {
            'filehash' : filehash,
        }
        if 'known_good' in kwargs:
            filedata['known_good'] = kwargs.get('known_good')

        return self.dbtable['file'].insert(filedata)


    def put_metadata(self, metadata_type, **kwargs):
        """ generic metadata inserter - only required thing is type to delineate from other fields - as it is the table name """
        if metadata_type not in self.dbtable:
            logger.debug(f"Metadata insert for a table that hasn't been used before: {metadata_type}")
            table = self.tinydb.table(name=metadata_type)
        else:
            table = self.dbtable.get(metadata_type)
        return table.insert(kwargs)
    
    def get_metadata(self, metadata_type, **kwargs):
        """ generic metadata getter
            only required thing is metadata_type to delineate from other fields - as it is the table name 
            
            kwargs should be search terms, beware this is likely a terrible implementation
            """
        if metadata_type not in self.dbtable:
            logger.debug(f"Metadata insert for a table that hasn't been used before: {metadata_type}")
            table = self.tinydb.table(name=metadata_type)
        else:
            table = self.dbtable.get(metadata_type)
        
        if len(kwargs) > 1:
            logger.warning("More than one search term provided, this only supports the first provided one for now!")
        
        if not kwargs: #pylint: disable=no-else-return
            logger.error("No search term provided, returning False")
            retval = False
        else:
            first_kwarg = list(kwargs.keys())[0]
            retval = table.search(Query()[first_kwarg] == kwargs[first_kwarg])
        return retval
    
    # TODO: dewar.metadata.put_hash del_hash ?