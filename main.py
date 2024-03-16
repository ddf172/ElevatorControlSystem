from System import *
from Gui import Application
import tkinter as tk

elevators_data = [
    Elevator(position=0, capacity=5),
    Elevator(position=2, capacity=5),
    Elevator(position=9, capacity=5),
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


# def main():
#   system = System(people_data, elevators_data, 10)
#   system.run_system()

def main():
    system = System(people_data, elevators_data, 10)
    root = tk.Tk()
    app = Application(master=root, system=system)
    app.mainloop()

if __name__ == "__main__":
    main()