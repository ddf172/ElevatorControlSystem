import tkinter as tk
from src.Visualization.Styles import AppStyles
from .BaseView import BaseView

class CustomView1(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Widok 1\n\nPrzykładowy\npierwszy widok",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)