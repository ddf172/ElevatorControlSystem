from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles


class CustomView2(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Widok 2\n\nPrzykładowy\ndrugi widok",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)