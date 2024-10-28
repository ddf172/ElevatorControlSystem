from .AbstractSettings import AbstractSettings


class Settings(AbstractSettings):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not self.__initialized:
            super().__init__()
            self.__initialized = True

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance
