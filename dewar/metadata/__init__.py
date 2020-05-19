""" base metadata store class """

from loguru import logger


from dewar.constants import METADATA_TYPES


class MetadataStore():
    """ base class for the metadata store """
    def __init__(self, **kwargs):
        pass

    def get_or_insert(self, metadata_type, **kwargs):
        """ get, and return, or insert and return a given piece of metadata """
        result = self.get(metadata_type, **kwargs)

        if not result:
            self.put(metadata_type, **kwargs)
            result = self.get(metadata_type, **kwargs)
        return result

    def get_hash(self, filehash: str):
        """ base implementation """
        raise NotImplementedError("This is the shell")

    def put_hash(self, filehash: str, **kwargs):
        """ base implementation """
        raise NotImplementedError("This is the shell")

    def put(self, metadata_type, **kwargs):
        """ generic metadata inserter - only required thing is type
            to delineate from other fields - as it is the table name """
        raise NotImplementedError("This is the shell")

    def get(self, metadata_type, **kwargs):
        """ generic metadata getter
            only required thing is metadata_type to delineate from other fields - as it is the table name

            kwargs should be search terms, beware this is likely a terrible implementation
            """
        raise NotImplementedError("This is the shell")

    # TODO: dewar.metadata.del_hash() ?
