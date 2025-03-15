import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ElevatorSystemGUI:
    def __init__(self, master=None, system=None):
        self.master = master
        self.system = system
        self.is_running = False
        self.animation_speed = 500  # milliseconds delay between animation steps

        # Path generation trackers
        self.steps_since_last_path_generation = 0
        self.steps_since_last_person_added = 0

        # Setup main window
        self.master.title("Elevator System Simulator")
        self.master.geometry("1200x800")
        self.master.configure(bg="#f0f0f0")

        # Initialize state trackers
        self.current_step = 0
        self.fitness_history = {
            'all_time_best': [],
            'current_best': [],
            'mean': [],
            'worst': []
        }
        self.path_history = {}
        self.elevator_colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
        for i in range(len(self.system.elevators)):
            self.path_history[i] = []

        # Configure styles
        self.configure_styles()

        # Create frames
        self.create_frames()

        # Create widgets in each frame
        self.create_control_panel()
        self.create_building_view()
        self.create_stats_panel()
        self.create_elevator_info_panel()

        # Update display
        self.update_display()

    def configure_styles(self):
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Configure button style
        self.style.configure("TButton",
                             font=("Arial", 10, "bold"),
                             background="#4CAF50",
                             foreground="black",
                             padding=5)

        # Configure frame style
        self.style.configure("TFrame", background="#f0f0f0")

        # Configure label style
        self.style.configure("TLabel",
                             font=("Arial", 10),
                             background="#f0f0f0",
                             foreground="black")

        # Configure heading style
        self.style.configure("Heading.TLabel",
                             font=("Arial", 12, "bold"),
                             background="#f0f0f0",
                             foreground="black")

    def create_frames(self):
        # Create main container
        self.main_container = ttk.Frame(self.master, style="TFrame")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Top frame for control panel
        self.control_frame = ttk.Frame(self.main_container, style="TFrame")
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Middle frame layout
        self.middle_frame = ttk.Frame(self.main_container, style="TFrame")
        self.middle_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Building view on the left
        self.building_frame = ttk.Frame(self.middle_frame, style="TFrame", relief="ridge", borderwidth=2)
        self.building_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Stats on the right
        self.stats_frame = ttk.Frame(self.middle_frame, style="TFrame", relief="ridge", borderwidth=2)
        self.stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Bottom frame for elevator details
        self.elevator_info_frame = ttk.Frame(self.main_container, style="TFrame", relief="ridge", borderwidth=2)
        self.elevator_info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_control_panel(self):
        # Title
        title_label = ttk.Label(self.control_frame, text="Elevator System Simulator",
                                font=("Arial", 16, "bold"), style="Heading.TLabel")
        title_label.pack(pady=5)

        # Control buttons
        self.button_frame = ttk.Frame(self.control_frame, style="TFrame")
        self.button_frame.pack(pady=10)

        # Step button
        self.step_button = ttk.Button(self.button_frame, text="Step", command=self.run_single_step)
        self.step_button.grid(row=0, column=0, padx=5)

        # Run/Pause button
        self.run_button = ttk.Button(self.button_frame, text="Run", command=self.toggle_run)
        self.run_button.grid(row=0, column=1, padx=5)

        # Reset button
        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.grid(row=0, column=2, padx=5)

        # Generate new path button
        self.generate_path_button = ttk.Button(self.button_frame, text="Generate New Path",
                                               command=self.generate_new_path)
        self.generate_path_button.grid(row=0, column=3, padx=5)

        # Add Person button
        self.add_person_button = ttk.Button(self.button_frame, text="Add Person",
                                            command=self.add_random_person)
        self.add_person_button.grid(row=0, column=4, padx=5)

        # Speed control
        speed_frame = ttk.Frame(self.control_frame, style="TFrame")
        speed_frame.pack(pady=5)

        speed_label = ttk.Label(speed_frame, text="Animation Speed:", style="TLabel")
        speed_label.grid(row=0, column=0, padx=5)

        self.speed_scale = ttk.Scale(speed_frame, from_=100, to=1000, orient=tk.HORIZONTAL,
                                     length=200, value=self.animation_speed,
                                     command=self.update_speed)
        self.speed_scale.grid(row=0, column=1, padx=5)

        self.speed_value_label = ttk.Label(speed_frame, text=f"{self.animation_speed} ms", style="TLabel")
        self.speed_value_label.grid(row=0, column=2, padx=5)

        # Status display
        status_frame = ttk.Frame(self.control_frame, style="TFrame")
        status_frame.pack(pady=5)

        self.runtime_label = ttk.Label(status_frame,
                                       text=f"Runtime Remaining: {self.system.settings.system.runtime}",
                                       style="TLabel")
        self.runtime_label.grid(row=0, column=0, padx=20)

        self.step_label = ttk.Label(status_frame, text=f"Current Step: {self.current_step}", style="TLabel")
        self.step_label.grid(row=0, column=1, padx=20)

        self.people_count_label = ttk.Label(status_frame,
                                            text=f"Waiting People: {self.system.people_manager.containers[None].count}",
                                            style="TLabel")
        self.people_count_label.grid(row=0, column=2, padx=20)

        self.transported_label = ttk.Label(status_frame,
                                           text=f"Transported People: {self.system.transported_people}",
                                           style="TLabel")
        self.transported_label.grid(row=0, column=3, padx=20)

        # Path generation tracking display
        path_tracking_frame = ttk.Frame(self.control_frame, style="TFrame")
        path_tracking_frame.pack(pady=5)

        self.path_gen_interval_label = ttk.Label(path_tracking_frame,
                                                 text=f"Path Generation Interval: {self.system.settings.system.path_generation_interval}",
                                                 style="TLabel")
        self.path_gen_interval_label.grid(row=0, column=0, padx=20)

        self.steps_since_path_gen_label = ttk.Label(path_tracking_frame,
                                                    text=f"Steps Since Last Path Generation: {self.steps_since_last_path_generation}",
                                                    style="TLabel")
        self.steps_since_path_gen_label.grid(row=0, column=1, padx=20)

        # Person adding tracking display (only shown if new_person_interval > 0)
        if self.system.settings.system.new_person_interval > 0:
            self.person_interval_label = ttk.Label(path_tracking_frame,
                                                   text=f"New Person Interval: {self.system.settings.system.new_person_interval}",
                                                   style="TLabel")
            self.person_interval_label.grid(row=1, column=0, padx=20)

            self.steps_since_person_label = ttk.Label(path_tracking_frame,
                                                      text=f"Steps Since Last Person Added: {self.steps_since_last_person_added}",
                                                      style="TLabel")
            self.steps_since_person_label.grid(row=1, column=1, padx=20)

    def create_building_view(self):
        # Building view title
        building_title = ttk.Label(self.building_frame, text="Building View", style="Heading.TLabel")
        building_title.pack(pady=5)

        # Canvas for building visualization
        canvas_height = 600
        canvas_width = 400

        self.building_canvas = tk.Canvas(self.building_frame, height=canvas_height,
                                         width=canvas_width, bg="white",
                                         relief="sunken", borderwidth=1)
        self.building_canvas.pack(pady=5, fill=tk.BOTH, expand=True)

        # Store canvas dimensions for drawing
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width

    def create_stats_panel(self):
        # Stats title
        stats_title = ttk.Label(self.stats_frame, text="System Statistics", style="Heading.TLabel")
        stats_title.pack(pady=5)

        # Create matplotlib figure for fitness graph
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.fitness_plot = self.figure.add_subplot(111)
        self.fitness_plot.set_title("Fitness Metrics Per Generation")
        self.fitness_plot.set_xlabel("Step")
        self.fitness_plot.set_ylabel("Fitness Value")

        # Canvas for matplotlib
        self.canvas = FigureCanvasTkAgg(self.figure, self.stats_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Current stats frame
        self.current_stats_frame = ttk.Frame(self.stats_frame, style="TFrame")
        self.current_stats_frame.pack(fill=tk.X, padx=5, pady=10)

        # Create stats labels
        self.all_time_best_label = ttk.Label(self.current_stats_frame,
                                             text="All-time Best Fitness: N/A",
                                             style="TLabel")
        self.all_time_best_label.pack(anchor=tk.W, pady=2)

        self.current_best_label = ttk.Label(self.current_stats_frame,
                                            text="Current Best Fitness: N/A",
                                            style="TLabel")
        self.current_best_label.pack(anchor=tk.W, pady=2)

        self.mean_fitness_label = ttk.Label(self.current_stats_frame,
                                            text="Mean Fitness: N/A",
                                            style="TLabel")
        self.mean_fitness_label.pack(anchor=tk.W, pady=2)

        self.worst_fitness_label = ttk.Label(self.current_stats_frame,
                                             text="Worst Fitness: N/A",
                                             style="TLabel")
        self.worst_fitness_label.pack(anchor=tk.W, pady=2)

        # People waiting stats
        self.people_waiting_label = ttk.Label(self.current_stats_frame,
                                              text="People Waiting: 0",
                                              style="TLabel")
        self.people_waiting_label.pack(anchor=tk.W, pady=2)

    def create_elevator_info_panel(self):
        # Elevator info title
        elevator_info_title = ttk.Label(self.elevator_info_frame,
                                        text="Elevator Information",
                                        style="Heading.TLabel")
        elevator_info_title.pack(pady=5)

        # Elevator info container (scrollable if needed)
        self.elevator_info_canvas = tk.Canvas(self.elevator_info_frame, borderwidth=0)
        self.elevator_info_scrollbar = ttk.Scrollbar(self.elevator_info_frame,
                                                     orient=tk.VERTICAL,
                                                     command=self.elevator_info_canvas.yview)
        self.elevator_info_container = ttk.Frame(self.elevator_info_canvas, style="TFrame")

        self.elevator_info_canvas.configure(yscrollcommand=self.elevator_info_scrollbar.set)

        self.elevator_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.elevator_info_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.elevator_info_canvas.create_window((0, 0), window=self.elevator_info_container,
                                                anchor=tk.NW, tags="self.elevator_info_container")

        self.elevator_info_container.bind("<Configure>", self.on_frame_configure)

        # Create frames for each elevator
        self.elevator_frames = []
        self.path_labels = []
        self.position_labels = []
        self.people_labels = []

        for i, elevator in enumerate(self.system.elevators):
            elevator_frame = ttk.Frame(self.elevator_info_container, style="TFrame",
                                       relief="groove", borderwidth=2)
            elevator_frame.pack(fill=tk.X, pady=5, padx=10)

            color_box = tk.Canvas(elevator_frame, width=20, height=20,
                                  bg=self.elevator_colors[i % len(self.elevator_colors)],
                                  highlightthickness=1, highlightbackground="black")
            color_box.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

            elevator_label = ttk.Label(elevator_frame,
                                       text=f"Elevator {i + 1}",
                                       font=("Arial", 11, "bold"))
            elevator_label.grid(row=0, column=1, sticky=tk.W, pady=2)

            position_label = ttk.Label(elevator_frame,
                                       text=f"Position: {elevator.state.position}")
            position_label.grid(row=1, column=1, sticky=tk.W, pady=2)

            path_label = ttk.Label(elevator_frame,
                                   text=f"Path: {elevator.state.path}")
            path_label.grid(row=1, column=2, sticky=tk.W, pady=2, padx=(20, 0))

            # People info
            people_text = self.get_people_text(i)
            people_label = ttk.Label(elevator_frame, text=f"People: {people_text}")
            people_label.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=2)

            self.elevator_frames.append(elevator_frame)
            self.position_labels.append(position_label)
            self.path_labels.append(path_label)
            self.people_labels.append(people_label)

    def on_frame_configure(self, event=None):
        # Reset the scroll region to encompass the inner frame
        self.elevator_info_canvas.configure(scrollregion=self.elevator_info_canvas.bbox("all"))

    def get_people_text(self, elevator_index):
        if elevator_index not in self.system.people_manager.containers:
            return "None"

        people_info = []
        for floor, people in self.system.people_manager.containers[elevator_index].floors.items():
            for person_id, person in people.items():
                people_info.append(f"ID:{person.id} ({person.start_pos}→{person.destination})")

        return ", ".join(people_info) if people_info else "None"

    def draw_building(self):
        self.building_canvas.delete("all")

        floor_count = self.system.settings.path.highest_floor - self.system.settings.path.lowest_floor + 1
        floor_height = self.canvas_height / floor_count

        # Draw floor lines
        for i in range(floor_count + 1):
            y = self.canvas_height - i * floor_height
            self.building_canvas.create_line(0, y, self.canvas_width, y, width=2)

            # Draw floor numbers
            if i < floor_count:
                floor_number = self.system.settings.path.lowest_floor + i
                self.building_canvas.create_text(20, y - floor_height / 2,
                                                 text=f"Floor {floor_number}",
                                                 font=("Arial", 10))

        # Draw shaft outlines
        elevator_count = len(self.system.elevators)
        shaft_width = min(70, (self.canvas_width - 50) / elevator_count)

        for i in range(elevator_count):
            x1 = 50 + i * (shaft_width + 20)
            x2 = x1 + shaft_width

            # Draw elevator shaft
            self.building_canvas.create_rectangle(x1, 0, x2, self.canvas_height, outline="gray", width=2)

            # Draw elevator number
            self.building_canvas.create_text(x1 + shaft_width / 2, 20,
                                             text=f"E{i + 1}",
                                             font=("Arial", 9, "bold"))

            # Draw elevator
            elevator = self.system.elevators[i]
            position = elevator.state.position

            # Calculate elevator position
            elevator_y = self.canvas_height - (position - self.system.settings.path.lowest_floor + 1) * floor_height

            # Draw elevator with its color
            color = self.elevator_colors[i % len(self.elevator_colors)]

            self.building_canvas.create_rectangle(x1 + 5, elevator_y + 5, x2 - 5, elevator_y + floor_height - 5,
                                                  fill=color, outline="black", width=2)

            # Show number of people in elevator
            people_count = self.system.people_manager.containers[i].count

            if people_count > 0:
                self.building_canvas.create_text(x1 + shaft_width / 2, elevator_y + floor_height / 2,
                                                 text=f"{people_count}",
                                                 font=("Arial", 10, "bold"),
                                                 fill="white")

        # Draw waiting people on each floor
        waiting_container = self.system.people_manager.containers[None]

        for floor in range(self.system.settings.path.lowest_floor, self.system.settings.path.highest_floor + 1):
            floor_y = self.canvas_height - (floor - self.system.settings.path.lowest_floor + 1) * floor_height

            if floor in waiting_container.floors and waiting_container.floors[floor]:
                people_count = len(waiting_container.floors[floor])

                # Draw people waiting icon
                x_pos = self.canvas_width - 30
                self.building_canvas.create_oval(x_pos - 10, floor_y + floor_height / 2 - 10,
                                                 x_pos + 10, floor_y + floor_height / 2 + 10,
                                                 fill="orange", outline="black")
                self.building_canvas.create_text(x_pos, floor_y + floor_height / 2,
                                                 text=f"{people_count}",
                                                 font=("Arial", 9, "bold"))

    def update_fitness_graph(self):
        # Check if we have an algorithm with evolution data
        if hasattr(self.system, 'algorithm') and hasattr(self.system.algorithm, 'fitness_evolution'):
            self.fitness_plot.clear()

            evolution = self.system.algorithm.fitness_evolution
            iterations = range(len(evolution['all_time_best']))

            # Plot each metric with different colors and labels
            if evolution['all_time_best']:
                self.fitness_plot.plot(iterations, evolution['all_time_best'], 'b-', label='All-time Best')
            if evolution['current_best']:
                self.fitness_plot.plot(iterations, evolution['current_best'], 'g-', label='Current Best')
            if evolution['mean']:
                self.fitness_plot.plot(iterations, evolution['mean'], 'y-', label='Mean')
            if evolution['worst']:
                self.fitness_plot.plot(iterations, evolution['worst'], 'r-', label='Worst')

            self.fitness_plot.set_title("Fitness Evolution Across Iterations")
            self.fitness_plot.set_xlabel("Iteration")
            self.fitness_plot.set_ylabel("Fitness Value")
            self.fitness_plot.legend(loc='best')

            # Set reasonable y-limits
            all_values = []
            for metric_values in evolution.values():
                all_values.extend([v for v in metric_values if v is not None])

            if all_values:
                min_fitness = min(all_values)
                max_fitness = max(all_values)
                padding = max(abs(max_fitness - min_fitness) * 0.1, 10)
                self.fitness_plot.set_ylim(min_fitness - padding, max_fitness + padding)

            # Update canvas
            self.canvas.draw()

    def update_elevator_info(self):
        # Update elevator information
        for i, elevator in enumerate(self.system.elevators):
            # Update position
            self.position_labels[i].config(text=f"Position: {elevator.state.position}")

            # Update path
            path_text = f"Path: {elevator.state.path}"
            self.path_labels[i].config(text=path_text)

            # Update people
            people_text = self.get_people_text(i)
            self.people_labels[i].config(text=f"People: {people_text}")

    def update_status_info(self):
        # Update status information
        self.runtime_label.config(text=f"Runtime Remaining: {self.system.settings.system.runtime}")
        self.step_label.config(text=f"Current Step: {self.current_step}")
        self.people_count_label.config(text=f"Waiting People: {self.system.people_manager.containers[None].count}")
        self.transported_label.config(text=f"Transported People: {self.system.transported_people}")

        # Update path generation tracking
        self.path_gen_interval_label.config(
            text=f"Path Generation Interval: {self.system.settings.system.path_generation_interval}")
        self.steps_since_path_gen_label.config(
            text=f"Steps Since Last Path Generation: {self.steps_since_last_path_generation}")

        # Update person adding tracking if enabled
        if self.system.settings.system.new_person_interval > 0:
            self.person_interval_label.config(
                text=f"New Person Interval: {self.system.settings.system.new_person_interval}")
            self.steps_since_person_label.config(
                text=f"Steps Since Last Person Added: {self.steps_since_last_person_added}")

        # Update fitness statistics if available
        if hasattr(self.system, 'algorithm') and hasattr(self.system.algorithm, 'generation_metrics'):
            metrics = self.system.algorithm.generation_metrics

            if metrics['all_time_best'] is not None:
                self.all_time_best_label.config(text=f"All-time Best Fitness: {metrics['all_time_best']:.2f}")

            if metrics['current_best'] is not None:
                self.current_best_label.config(text=f"Current Best Fitness: {metrics['current_best']:.2f}")

            if metrics['mean'] is not None:
                self.mean_fitness_label.config(text=f"Mean Fitness: {metrics['mean']:.2f}")

            if metrics['worst'] is not None:
                self.worst_fitness_label.config(text=f"Worst Fitness: {metrics['worst']:.2f}")

        self.people_waiting_label.config(text=f"People Waiting: {self.system.people_manager.containers[None].count}")

    def update_display(self):
        # Update all display elements
        self.draw_building()
        self.update_elevator_info()
        self.update_status_info()
        self.update_fitness_graph()

    def check_and_regenerate_paths(self, force=False):
        """Check if paths need to be regenerated based on system settings"""
        path_generation_needed = False

        # Check if path generation interval has been reached
        if self.steps_since_last_path_generation >= self.system.settings.system.path_generation_interval:
            path_generation_needed = True

        # Check if any elevator has an empty path
        for elevator in self.system.elevators:
            if not elevator.state.path:
                path_generation_needed = True
                break

        # Generate new paths if needed or forced
        if path_generation_needed or force:
            try:
                print(f"Generating new path at step {self.current_step}")
                self.system.make_path()
                self.steps_since_last_path_generation = 0
                return True
            except Exception as e:
                print(f"Error generating path: {e}")
                return False

        return False

    def check_and_add_people(self):
        """Check if new people should be added based on system settings"""
        # Check if new person interval is set and has been reached
        if (self.system.settings.system.new_person_interval > 0 and
                self.steps_since_last_person_added >= self.system.settings.system.new_person_interval):

            # Add batch of people
            for i in range(self.system.settings.system.people_batch_size):
                self.system.add_person()

            self.steps_since_last_person_added = 0

            # Regenerate paths when new people are added
            self.check_and_regenerate_paths(force=True)

            return True

        return False

    def run_single_step(self):
        # Run a single step of the simulation
        if self.system.settings.system.runtime > 0:
            # Check if new people should be added
            self.check_and_add_people()

            # Check if paths need to be regenerated
            path_regenerated = self.check_and_regenerate_paths()

            try:
                # Make a move
                self.system.make_move()

                # Update paths history (keep this part for elevator path visualization)
                for i, elevator in enumerate(self.system.elevators):
                    if i in self.path_history:
                        self.path_history[i].append(elevator.state.path.copy() if elevator.state.path else [])

                # Update counters
                self.current_step += 1
                self.system.settings.system.runtime -= 1
                self.steps_since_last_path_generation += 1
                self.steps_since_last_person_added += 1

                # Update display
                self.update_display()

            except AssertionError:
                # Handle case when elevator has no path
                print("Regenerating paths as at least one elevator has an empty path")
                self.check_and_regenerate_paths(force=True)
                self.update_display()

    def toggle_run(self):
        # Toggle between running and paused states
        self.is_running = not self.is_running

        if self.is_running:
            self.run_button.config(text="Pause")
            self.run_continuous()
        else:
            self.run_button.config(text="Run")

    def run_continuous(self):
        # Run simulation continuously until paused or completed
        if self.is_running and self.system.settings.system.runtime > 0:
            self.run_single_step()
            self.master.after(int(self.animation_speed), self.run_continuous)
        elif self.system.settings.system.runtime <= 0:
            self.is_running = False
            self.run_button.config(text="Run")

    def generate_new_path(self):
        # Generate new paths for elevators
        self.check_and_regenerate_paths(force=True)
        self.update_display()

    def add_random_person(self):
        # Add a random person to the system
        self.system.add_person()
        # Regenerate paths when manually adding a person
        self.check_and_regenerate_paths(force=True)
        self.update_display()

    def reset_simulation(self):
        # Reset simulation state
        self.is_running = False
        self.run_button.config(text="Run")

        # Reset system runtime
        self.system.settings.system.runtime = 100  # or whatever initial value

        # Reset counters
        self.current_step = 0
        self.steps_since_last_path_generation = 0
        self.steps_since_last_person_added = 0

        # Reset path history
        for i in range(len(self.system.elevators)):
            self.path_history[i] = []

        # Generate new paths
        self.check_and_regenerate_paths(force=True)

        # Update display
        self.update_display()

    def update_speed(self, value):
        # Update animation speed
        self.animation_speed = int(float(value))
        self.speed_value_label.config(text=f"{self.animation_speed} ms")


def run_gui():
    # Import needed modules
    from src.System import System
    from src.Objects.Elevator import SystemElevator
    from src.Objects.Person import Person

    # Create sample data similar to main.py
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

    # Create system
    system = System(elevators_data, people_data)

    # Configure system settings for the GUI demo
    # Uncomment and modify these lines to test different settings
    # system.settings.system.new_person_interval = 10
    # system.settings.system.people_batch_size = 2
    # system.settings.system.path_generation_interval = 5

    # Initialize paths
    system.make_path()

    # Create and run GUI
    root = tk.Tk()
    app = ElevatorSystemGUI(master=root, system=system)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
