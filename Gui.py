import tkinter as tk
from System import System

class Application(tk.Frame):
    def __init__(self, master=None, system=None):
        super().__init__(master)
        self.master = master
        self.system = system
        self.pack()
        self.create_widgets()
        self.when_to_add_person = 0
        self.when_to_generate_path = 0

    def create_widgets(self):
        self.system_state = tk.Label(self)
        self.system_state.pack(anchor='w')

        self.run_iteration_button = tk.Button(self, text="Run Iteration", command=self.run_iteration)
        self.run_iteration_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.update_system_state()

    def run_iteration(self):

        if self.system.runtime > 0:
            self.system.runtime -= 1
            self.when_to_add_person += 1
            if self.when_to_add_person == self.system.new_person_in_moves:
                for i in range(self.system.how_many_people_at_once):
                    self.system.add_person()

                self.system.make_path()
                self.when_to_add_person = 0
                self.when_to_generate_path = 0

            if self.when_to_generate_path == self.system.how_often_generate_new_path:
                self.system.make_path()
                self.when_to_generate_path = 0

            self.when_to_generate_path += 1
            self.system.make_move()
            self.update_system_state()

    def update_system_state(self):
        self.system_state["text"] = self.get_system_state()

    def get_system_state(self):
        state = f"Runtime: {self.system.runtime}\n"
        state += "Elevators:\n"
        for i, elevator in enumerate(self.system.elevators):
            state += f"  Elevator {i + 1}:\n"
            state += f"    Position: {elevator.position}\n"
            state += f"    People: {[person.id for person in elevator.people]}\n"

        state += "People waiting:\n"
        for person in self.system.people:
            state += f"  Person ID: {person.id}, Start Position: {person.start_pos}, Destination: {person.destination}\n"

        state += "People in elevators:\n"
        for i, elevator in enumerate(self.system.elevators):
            for person in elevator.people:
                state += f"  Elevator {i + 1}, Person ID: {person.id}, Start Position: {person.start_pos}, Destination: {person.destination}\n"

        state += "\nBuilding state:\n"
        building_state = self.get_building_state()
        for floor_state in building_state:
            state += floor_state + "\n"

        return state

    def get_building_state(self):
        building_state = []
        for floor in range(self.system.floor_number - 1, -1, -1):
            floor_str = ""
            for elevator in self.system.elevators:
                if elevator.position == floor:
                    floor_str += "E"
                else:
                    floor_str += "o"
            building_state.append(floor_str)
        return building_state