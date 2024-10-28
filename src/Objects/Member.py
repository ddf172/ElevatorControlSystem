from typing import List
from src.Settings.Settings import Settings
from src.Objects.Elevator import AlgorithmElevator


class Member:
    def __init__(self):
        self.elevators: List[AlgorithmElevator] = []
        self.fitness: int = 0
        self.settings = Settings()

    def add_elevator(self, elevator: AlgorithmElevator) -> None:
        if len(self.elevators) == self.settings.get_elevator_number():
            raise (ValueError("Member already has 3 elevators"))

        if type(elevator) is not AlgorithmElevator:
            raise (TypeError("Object is not of type Elevator"))
        if elevator in self.elevators:
            raise (ValueError("Elevator already in list"))
        self.elevators.append(elevator)

    def get_elevator(self, index: int) -> AlgorithmElevator:
        if index < 0 or index >= len(self.elevators):
            raise (IndexError("Index out of range"))
        return self.elevators[index]
