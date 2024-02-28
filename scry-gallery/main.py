import customtkinter as ctk

from controller import Controller
from ui.appframe import AppFrame

if __name__ == "__main__":
    window = ctk.CTk()
    app = AppFrame(master=window)
    controller = Controller(app)

    app.pack(fill='both', expand=True)

    window.mainloop()
