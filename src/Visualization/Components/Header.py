import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from src.Visualization.Styles import AppStyles


class Header:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.setup_labels()

    def setup_labels(self):
        font = tkfont.Font(size=11)
        self.info_label = ttk.Label(
            self.frame,
            text="Informations",
            font=font,
            background=AppStyles.COLORS['background']
        )
        self.control_label = ttk.Label(
            self.frame,
            text="Controls",
            font=font,
            background=AppStyles.COLORS['background']
        )

        self.info_label.pack(side=tk.LEFT)
        self.control_label.pack(side=tk.RIGHT)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)