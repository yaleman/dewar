""" dewar, a storage place for samples of all kinds """

from loguru import logger

class Dewar():
    """ app class """
    def __init__(self, **kwargs):
        self.storage_backend = kwargs.get('storage_backend')
        self.storage_incoming_other = kwargs['storage_incoming_other']
        self.storage_incoming_knowngood = kwargs['storage_incoming_knowngood']
        self.frontend = kwargs.get('frontend')
        self.ingestor = kwargs.get('Ingestor')

    def __str__(self):
        return "Dewar as a string"

    def get_incoming_files(self):
        """ returns a dict of the files in the "incoming" storage backends """

        logger.debug(self.storage_incoming_knowngood)
        logger.debug(self.storage_incoming_other)
        return {
            'knowngood' : self.storage_incoming_knowngood.dir(),
            'other' : self.storage_incoming_other.dir(),
        }
