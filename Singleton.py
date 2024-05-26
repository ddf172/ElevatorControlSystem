class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls in cls._instances:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]
