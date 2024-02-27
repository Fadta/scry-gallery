from typing import Any, Callable, Tuple, List
from PIL import Image
import customtkinter as ctk


class Gallery(ctk.CTkScrollableFrame):
    def __init__(self, master:Any, rowLength: int, imgWidth: int, imgHeight:int, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        # fields
        self._rowLength = rowLength
        self._imgWidth = imgWidth
        self._imgHeight = imgHeight
        self._clickCallbacks: List[Callable] = []
        self._hoverCallbacks: List[Callable] = []
        
        self._lastUsedColumn = 0
        self._lastUsedRow = 0

        self._images: List[Tuple[Image.Image, str]] = []
        self._selectedIndex = 0
        self._hoveredImageIndex = 0


    def _updateSelectedIndex(self, newIx: int) -> None:
        self._selectedIndex = newIx
        

    def _imgClicked(self, clickedImgIndex: int) -> None:
        self._updateSelectedIndex(clickedImgIndex)
        for callback in self._clickCallbacks:
            callback()


    def _updateHoveredImage(self, newIx: int) -> None:
        self._hoveredImageIndex = newIx


    def _imgHovered(self, hoveredImgIx: int) ->  None:
        self._updateHoveredImage(hoveredImgIx)
        for callback in self._hoverCallbacks:
            callback()


    def _checkForRowJump(self):
        if self._lastUsedColumn >= self._rowLength:
            self._lastUsedColumn = 0
            self._lastUsedRow += 1


    def _placeNextInGrid(self, imgButton: ctk.CTkButton) -> None:
        self._checkForRowJump()
        imgButton.grid(row=self._lastUsedRow, column=self._lastUsedColumn)
        self._lastUsedColumn += 1


    def onImageClicked(self, callback: Callable) -> None:
        """
        Stores a callback to be called when an image is clicked

        Args:
            callback: Callable object with zero parameters to be called
        """
        self._clickCallbacks.append(callback)


    def onImageHover(self, callback: Callable) -> None:
        self._hoverCallbacks.append(callback)


    def getSelectedImage(self):
        return self.getImage(self.getSelectedIndex())


    def getSelectedIndex(self) -> int:
        return self._selectedIndex


    def getHoveredIndex(self) -> int:
        return self._hoveredImageIndex


    def getHoveredImage(self) -> Image.Image:
        return self._images[self.getHoveredIndex()][0]


    def getHoveredId(self) -> str:
        return self._images[self.getHoveredIndex()][1]


    def getImage(self, ix: int) -> Image.Image | None:
        if ix>=0 and ix<len(self._images):
            return self._images[ix][0]
        else:
            return None


    def getId(self, ix: int) -> str | None:
        if ix>=0 and ix<len(self._images):
            return self._images[ix][1]
        else:
            return None

        
    def addImage(self, img: Image.Image, id: str='auto') -> None:
        """
        Adds an image to the gallery, placing it in the grid
        Args:
            img: Image to be shown
            id: Identifier for the given image. If id='auto' id will be the index position
        """
        lastIndex = len(self._images)
        if id == 'auto':
            id = str(lastIndex)

        ctkImage = ctk.CTkImage(img, size=(self._imgWidth,self._imgHeight))
        imgButton = ctk.CTkButton(self,
                border_width=0,
                fg_color="transparent",
                border_spacing=0,
                text="",
                corner_radius=0,
                image=ctkImage,
                command=lambda: self._imgClicked(lastIndex)
        )
        imgButton.bind("<Enter>", lambda e, m=lastIndex: self._imgHovered(m))

        imageIdTuple = (img, id)
        self._images.append(imageIdTuple)
        self._placeNextInGrid(imgButton)


    def clear(self) -> None:
        """
        Clear all drawn images
        """
        for imgButton in self.winfo_children():
            imgButton.destroy()
        self._images.clear()

        self._lastUsedColumn = 0
        self._lastUsedRow = 0


if __name__ == "__main__":
    # window
    root = ctk.CTk()
    root.geometry("1600x900")
    root.title("Gallery test")

    # Images
    cardImg = Image.open("./resources/mkc-88-swords-to-plowshares.png")

    # add Gallery
    gallery = Gallery(root, rowLength=5, imgWidth=100, imgHeight=140)
    gallery.pack(fill='both', expand=True)

    # add images
    gallery.addImage(cardImg, "swords to plowshares")
    gallery.addImage(cardImg, "otra")
    gallery.addImage(cardImg, "XD")
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)
    gallery.addImage(cardImg)

    gallery.onImageClicked(lambda: print(gallery.getId(gallery.getSelectedIndex())))

    # loop
    root.mainloop()
