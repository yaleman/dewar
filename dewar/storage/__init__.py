""" base class for storage backend """

class Storage():
    """ base storage class """
    def __init__(self, **kwargs):
        """ base storage class """
        self.bucket = kwargs.get('bucket')
        self.metadatastore = kwargs.get('metadatastore')

    def get(self, filename: str):
        """ get a file by its hash, returns a dict:

            {
                'content' : bytes = the file content,
                'size' : int = file size,
            }
        """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def put(self, filename: str, contents: bytes, **kwargs: dict):
        """ put a file """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def update(self, filename: str, **kwargs: dict):
        """ update a file or its metadata """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def head(self, filename: str, **kwargs: dict):
        """ grab the metadata for a file and/or check the file exists """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def delete(self, filename: str, **kwargs: dict):
        """ delete a file

            if you pass bucket as an arg you can remove things from somewhere else,
                which is useful for ingestion etc
        """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def search(self, **kwargs: dict):
        """ search for files by size or type """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def dir(self, bucket: str, **kwargs: dict):
        """ list files in a storage location """
        raise NotImplementedError("This is a parent class for a proper implementation")
