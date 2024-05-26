from Singleton import Singleton


class Setting(Singleton):

    def __init__(self):
        if hasattr(self, 'initialized'): return
        self.initialized = True
