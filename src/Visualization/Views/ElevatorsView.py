from .BaseView import BaseView
import tkinter as tk
from src.Visualization.Styles import AppStyles


class ElevatorsView(BaseView):
    def setup_view(self):
        tk.Label(self.frame,
                 text="Panel wind\n\nTutaj będzie panel\nkontrolny wind",
                 font=('Arial', 14),
                 bg=AppStyles.COLORS['background']).pack(expand=True)