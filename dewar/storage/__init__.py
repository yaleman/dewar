""" base class for storage backend """

class DewarStorage():
    def __init__(self, metadatastore, bucket, **kwargs):
        pass

    def get(self, filehash: str):
        """ get a file by its hash, returns a dict:
        
            {
                'content' : bytes = the file content,
                'size' : int = file size,
            }
        """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def put(self, filehash: str, contents: bytes, metadata: dict):
        """ put a file """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def update(self, filehash: str, **kwargs: dict):
        """ update a file or its metadata """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def head(self, filehash: str):
        """ grab the metadata for a file and/or check the file exists """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def delete(self, filehash: str):
        """ delete a file """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def search(self, **kwargs: dict):
        """ search for files by size or type """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def dir(self, bucket: str):
        """ list files in a storage bucket """
        raise NotImplementedError("This is a parent class for a proper implementation")

