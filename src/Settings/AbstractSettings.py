from abc import ABC
from .SettingsSubclasses import *


class AbstractSettings(ABC):
    def __init__(self):
        self.path = SettingsPath()
        self.fitness = SettingsFitness()
        self.algorithm = SettingsAlgorithm()
        self.elevator = SettingsElevator()
        self.system = SettingsSystem()

    def get_path_length(self):
        return self.path.path_length

    def get_elevator_number(self):
        return self.elevator.elevator_number

    def get_lowest_floor(self):
        return self.path.lowest_floor

    def get_highest_floor(self):
        return self.path.highest_floor
