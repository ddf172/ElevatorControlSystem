from tkinter import ttk
import tkinter.font as tkfont


class AppStyles:
    COLORS = {
        'sidebar': '#2c3e50',
        'sidebar_hover': '#34495e',
        'background': '#f0f0f0',
        'text': 'black',
    }

    @staticmethod
    def setup_styles():
        style = ttk.Style()

        style.configure('Modern.TFrame',
                        background=AppStyles.COLORS['background'])
        style.configure('Sidebar.TFrame',
                        background=AppStyles.COLORS['sidebar'])

        style.configure('Modern.TButton',
                        padding=10,
                        background=AppStyles.COLORS['sidebar'],
                        foreground=AppStyles.COLORS['text'])
        style.map('Modern.TButton',
                  background=[('active', AppStyles.COLORS['sidebar_hover'])],
                  foreground=[('active', AppStyles.COLORS['text'])])

        return style