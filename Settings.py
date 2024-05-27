from Singleton import Singleton


class Settings(Singleton):

    def __init__(self):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self._path_length = 10
        self._elevator_number = 3

        self._lowest_floor = 0
        self._highest_floor = 10

    def get_path_length(self):
        return self._path_length

    def get_elevator_number(self):
        return self._elevator_number

    def get_lowest_floor(self):
        return self._lowest_floor

    def get_highest_floor(self):
        return self._highest_floor
