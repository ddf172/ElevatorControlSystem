import tkinter as tk
from tkinter import ttk
from Styles import AppStyles
from Components.Sidebar import Sidebar
from Components.Header import Header
from Components.MainContent import MainContent


class ModernSidebarApp:
    def __init__(self, root):
        self.root = root
        self.setup_root()
        self.setup_styles()
        self.setup_layout()

    def setup_root(self):
        self.root.title("Elevator Control System")
        self.root.geometry("800x600")
        self.root.configure(background=AppStyles.COLORS['background'])

    def setup_styles(self):
        self.style = AppStyles.setup_styles()

    def handle_button_click(self, view_name):
        self.main_content.show_view(view_name)

    def setup_layout(self):
        self.main_container = ttk.Frame(self.root, style='Modern.TFrame')
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.content_container = ttk.Frame(self.main_container, style='Modern.TFrame')
        self.content_container.pack(fill=tk.BOTH, expand=True)

        self.right_side = ttk.Frame(self.content_container, style='Modern.TFrame')

        self.main_content = MainContent(self.right_side)
        self.sidebar = Sidebar(self.content_container, self.handle_button_click)

        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.right_side.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.header = Header(self.right_side)
        self.header.pack(fill=tk.X, padx=20, pady=10)

        self.main_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)