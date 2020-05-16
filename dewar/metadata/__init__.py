""" base metadata store class """

class MetadataStore():
    """ base class for the metadata store """
    def __init__(self):
        pass

    def get(self, filehash: str):
        """ base implementation """
        pass
    
    def put(self, filehash: str):
        """ base implementation """
        pass