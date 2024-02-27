from tkinter import mainloop
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

    
    def show(self, image: Image.Image):
        ctkImage = ctk.CTkImage(image, size=(self.width, self.height))
        self.configure(image=ctkImage)


    def resetDisplay(self):
        self.configure(image=self.placeholder)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1600x900")

    
    #img
    voloImg = Image.open("./resources/clb-103-volo-itinerant-scholar.png")
    plowsharesImg = Image.open("./resources/mkc-88-swords-to-plowshares.png")

    imgdisplay = ImageDisplay(master=root, placeholder=voloImg, height= 560, width=400)
    updateBtn = ctk.CTkButton(master=root, text='update', command=lambda: imgdisplay.show(plowsharesImg))
    resetBtn = ctk.CTkButton(master=root, text='reset', command=imgdisplay.resetDisplay)

    imgdisplay.pack()
    updateBtn.pack()
    resetBtn.pack()

    root.mainloop()
