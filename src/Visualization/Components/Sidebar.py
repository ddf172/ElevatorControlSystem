import tkinter as tk
from tkinter import ttk
from src.Visualization.Styles import AppStyles


class Sidebar:
    def __init__(self, parent, on_button_click):
        self.frame = ttk.Frame(parent, style='Sidebar.TFrame')
        self.on_button_click = on_button_click
        self.setup_canvas()
        self.setup_buttons()

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.frame,
                                width=200,
                                background=AppStyles.COLORS['sidebar'],
                                highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame,
                                       orient="vertical",
                                       command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Sidebar.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0),
                                  window=self.scrollable_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def setup_buttons(self):
        menu_items = ["Stats", "People", "Elevators", "Functions", "View 1", "View 2"]
        self.buttons = {}
        for item in menu_items:
            self.buttons[item] = ttk.Button(
                self.scrollable_frame,
                text=item,
                style='Modern.TButton',
                width=25,
                command=lambda i=item: self.on_button_click(i)
            )
            self.buttons[item].pack(pady=2, padx=5)

    def pack(self, **kwargs):
        self.canvas.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame.pack(**kwargs)