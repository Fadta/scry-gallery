from typing import Any
from PIL import Image
import customtkinter as ctk


class ImageDisplay(ctk.CTkLabel):
    def __init__(self, master: Any, placeholder: Image.Image, width: int, height: int, **kwargs):
        super().__init__(master=master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.placeholder = ctk.CTkImage(placeholder, size=(self.width, self.height))
        self.configure(image=self.placeholder, text='')


    def show(self, image: Image.Image | None):
        if image is None:
            self.resetDisplay()

        else:
            ctkImage = ctk.CTkImage(image, size=(self.width, self.height))
            self.configure(image=ctkImage)


    def resetDisplay(self):
        self.configure(image=self.placeholder)
