from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles
from tkinter import ttk
from src.Settings.Settings import Settings


class PersonWidget(tk.Canvas):
    def __init__(self, parent, person, size=30):
        super().__init__(parent, width=size, height=size,
                         bg=AppStyles.COLORS['background'],
                         highlightthickness=0)
        self.size = size
        self.draw_person(person)

    def draw_person(self, person):
        padding = 2
        self.create_oval(padding, padding,
                         self.size - padding, self.size - padding,
                         fill="#B0BEC5", outline="#78909C")

        # ID
        self.create_text(self.size / 2, self.size / 3,
                         text=f"ID:{person.id}",
                         font=("Arial", int(self.size / 4)))

        # destination
        self.create_text(self.size / 2, 2 * self.size / 3,
                         text=f"→{person.destination}",
                         font=("Arial", int(self.size / 4)))


class PeopleContainer(ttk.Frame):
    def __init__(self, parent, max_people_per_row=5):
        super().__init__(parent, style='Modern.TFrame')
        self.max_per_row = max_people_per_row

    def update_people(self, people_dict):
        # Clear current widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Organize people in rows
        current_row = None
        for i, person in enumerate(people_dict.values()):
            if i % self.max_per_row == 0:
                current_row = ttk.Frame(self, style='Modern.TFrame')
                current_row.pack(fill=tk.X, pady=2)

            person_widget = PersonWidget(current_row, person)
            person_widget.pack(side=tk.LEFT, padx=2)


class ElevatorSystemView(ttk.Frame):
    def __init__(self, parent, floor_range, elevator_count):
        super().__init__(parent, style='Modern.TFrame')
        self.floor_range = floor_range
        self.elevator_count = elevator_count
        self.setup_grid()

    def setup_grid(self):
        # Headers
        ttk.Label(self, text="Floor",
                  style='Header.TLabel',
                  background=AppStyles.COLORS['background']).grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self, text="Waiting",
                  style='Header.TLabel',
                  background=AppStyles.COLORS['background']).grid(row=0, column=1, padx=5, pady=5)

        for i in range(self.elevator_count):
            ttk.Label(self, text=f"Elevator {i + 1}",
                      style='Header.TLabel',
                      background=AppStyles.COLORS['background']).grid(row=0, column=i + 2, padx=5, pady=5)

        # Elevators and waiting containers
        self.containers = {}

        # From highest to lowest floor
        for floor_idx, floor in enumerate(range(self.floor_range[1], self.floor_range[0] - 1, -1)):
            row = floor_idx + 1

            # Floor label
            ttk.Label(self, text=f"{floor}",
                      style='Floor.TLabel',
                      background=AppStyles.COLORS['background']).grid(row=row, column=0, padx=5, pady=2, sticky='e')

            # Waiting container
            waiting_container = PeopleContainer(self)
            waiting_container.grid(row=row, column=1, padx=5, pady=2, sticky='ew')
            self.containers[(None, floor)] = waiting_container

            # Elevator containers
            for elevator in range(self.elevator_count):
                elevator_container = PeopleContainer(self)
                elevator_container.grid(row=row, column=elevator + 2, padx=5, pady=2, sticky='ew')
                self.containers[(elevator, floor)] = elevator_container

        # Columns stretch configuration
        for i in range(self.elevator_count + 2):
            self.grid_columnconfigure(i, weight=1)


class PeopleView(BaseView):
    def setup_view(self):
        self.settings = Settings()
        floor_range = (self.settings.path.lowest_floor, self.settings.path.highest_floor)

        # Main container
        self.main_container = ttk.Frame(self.frame, style='Modern.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Elevator system
        self.elevator_system = ElevatorSystemView(
            self.main_container,
            floor_range,
            self.settings.elevator.elevator_number
        )
        self.elevator_system.pack(fill=tk.BOTH, expand=True)

    def update_view(self, people_manager):
        # Update waiting people
        for floor, people in people_manager.containers[None].floors.items():
            if (None, floor) in self.elevator_system.containers:
                self.elevator_system.containers[(None, floor)].update_people(people)

        # Update people in elevators
        for elevator_id in range(self.settings.elevator.elevator_number):
            for floor, people in people_manager.containers[elevator_id].floors.items():
                if (elevator_id, floor) in self.elevator_system.containers:
                    self.elevator_system.containers[(elevator_id, floor)].update_people(people)
