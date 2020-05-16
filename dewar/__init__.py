""" dewar, a storage place for samples of all kinds """

class Dewar():
    """ app class """
    def __init__(self, **kwargs):
        self.storage_backend = kwargs.get('storage_backend')
        self.frontend = kwargs.get('frontend')
