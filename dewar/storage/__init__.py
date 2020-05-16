""" base class for storage backend """

class DewarStorage():
    def __init__(self):
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

    def patch(self, filehash: str, contents: bytes = None, metadata: dict = None):
        """ update a file or its metadata """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def head(self, filehash: str):
        """ grab the metadata for a file and/or check the file exists """
        raise NotImplementedError("This is a parent class for a proper implementation")

    def delete(self, filehash: str):
        """ delete a file """
        raise NotImplementedError("This is a parent class for a proper implementation")

