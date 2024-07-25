from Singleton import Singleton
from SettingsSubclasses import *


class Settings(Singleton):

    def __init__(self):
        if hasattr(self, 'initialized'): return
        self.initialized = True

        self.elevator_number = 3
        self.elevator_capacity = 5

        self.path = SettingsPath()
        self.fitness = SettingsFitness()
        self.algorithm = SettingsAlgorithm()

    def get_path_length(self):
        return self.path.path_length

    def get_elevator_number(self):
        return self.elevator_number

    def get_lowest_floor(self):
        return self.path.lowest_floor

    def get_highest_floor(self):
        return self.path.highest_floor
