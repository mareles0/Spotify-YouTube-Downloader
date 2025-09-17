import customtkinter as ctk
from gui.main_window import DownloaderApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = DownloaderApp(root)
    root.mainloop()
