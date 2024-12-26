from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles


class PeopleView(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Lista osób\n\nTutaj będzie lista\nużytkowników systemu",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)
