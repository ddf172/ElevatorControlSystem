from tkinter import ttk
from src.Visualization.Views import *


class MainContent:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.current_view = None
        self.views = {}
        self.setup_views()

    def setup_views(self):
        self.views = {
            'Stats': StatsView(self.frame),
            'People': PeopleView(self.frame),
            'Elevators': ElevatorsView(self.frame),
            'Functions': FunctionsView(self.frame),
            'View 1': CustomView1(self.frame),
            'View 2': CustomView2(self.frame)
        }

    def show_view(self, view_name):
        if self.current_view:
            self.current_view.hide()

        self.current_view = self.views[view_name]
        self.current_view.show()

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self.show_view('Stats')