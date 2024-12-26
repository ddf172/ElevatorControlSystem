from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles


class FunctionsView(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Funkcje\n\nTutaj będą dodatkowe\nfunkcje systemu",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)