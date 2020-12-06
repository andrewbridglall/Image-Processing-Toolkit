import tkinter as tk
from modules.launch_window import LaunchWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Andrew's Awesome Image Processor!")
    LaunchWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
