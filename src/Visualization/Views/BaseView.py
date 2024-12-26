from tkinter import ttk
from abc import ABC


class BaseView(ABC):
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.setup_view()

    def setup_view(self):
        pass

    def show(self):
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)

    def hide(self):
        self.frame.pack_forget()
