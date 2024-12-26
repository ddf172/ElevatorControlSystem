from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles


class StatsView(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Statystyki\n\nTutaj będą wyświetlane\nstatystyki aplikacji",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)