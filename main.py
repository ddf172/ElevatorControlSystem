from src.System.System import *

elevators_data = [
    SystemElevator(position=0),
    SystemElevator(position=2),
    SystemElevator(position=9),
]

people_data = [
    Person(start_pos=0, destination=5),
    Person(start_pos=3, destination=1),
    Person(start_pos=6, destination=0),
    Person(start_pos=1, destination=4),
    Person(start_pos=2, destination=0),
    Person(start_pos=4, destination=7),
    Person(start_pos=5, destination=2),
    Person(start_pos=8, destination=3),
    Person(start_pos=7, destination=1),
    Person(start_pos=0, destination=9),
    Person(start_pos=2, destination=1),
    Person(start_pos=6, destination=3),
]


def main():
    system = System(elevators_data, people_data)
    system.run_system()


if __name__ == "__main__":
    main()
