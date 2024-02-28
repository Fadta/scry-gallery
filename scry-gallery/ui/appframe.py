import customtkinter as ctk
from PIL import Image
from ui.gallery import Gallery
from ui.display import ImageDisplay

class AppFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, **kwargs) -> None:
        super().__init__(master=master, **kwargs)

        self.width=1600
        self.height=900

        galleryLength = 5

        self.artGallery = Gallery(master=self, rowLength=galleryLength, imgWidth=137, imgHeight=100)
        self.artDisplay = ImageDisplay(master=self, placeholder=Image.open("./ui/resources/art_404.png"), height=219, width=300)

        self.cardGallery = Gallery(master=self, rowLength=galleryLength, imgWidth=100, imgHeight=140)
        self.cardDisplay = ImageDisplay(master=self, placeholder=Image.open("./ui/resources/card_404.png"), height=420, width=300)
        
        self.textField = ctk.CTkTextbox(master=self)

        self.startBtn = ctk.CTkButton(master=self, text="Run")
        self.statusLbl = ctk.CTkLabel(master=self, text="Prepared to run", text_color="green yellow")
        self.cardName = ctk.CTkLabel(master=self, text="Card Name", text_color="turquoise1")


        # frame configuration
        master.geometry(f"{self.width}x{self.height}")
        master.resizable(False, False)
        master.title("Scry-Gallery")

        self._buildGrid()

        # bind events on gallery to corresponding display updates
        self.artGallery.onImageHover(lambda: self.artDisplay.show(
                self.artGallery.getHoveredImage()
            ))

        self.cardGallery.onImageHover(lambda: self.cardDisplay.show(
                self.cardGallery.getHoveredImage()
            ))


    def _buildGrid(self) -> None:
        INTERNAL_PADDING = 20
        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1), weight=1)

        self.textField.grid(row=0, column=0, rowspan=2, padx=INTERNAL_PADDING, pady=INTERNAL_PADDING, sticky='wesn')
        
        self.artGallery.grid(row=0, column=1, columnspan=3, pady=INTERNAL_PADDING, sticky='wesn')
        self.artDisplay.grid(row=0, column=4, sticky='wesn')

        self.cardGallery.grid(row=1, column=1, columnspan=3, pady=INTERNAL_PADDING, sticky='wesn')
        self.cardDisplay.grid(row=1, column=4, sticky='wesn')

        self.startBtn.grid(row=2, column=0, padx=INTERNAL_PADDING, sticky='wesn')
        self.cardName.grid(row=2, column=4)
        self.statusLbl.grid(row=2, column=1, columnspan=3)


    def setCardName(self, name: str) -> None:
        self.cardName.configure(text=name)


    def setStatus(self, status: str) -> None:
        self.statusLbl.configure(text=status)
        

    def addArt(self, img: Image.Image, artistName: str) -> None:
        self.artGallery.addImage(img, artistName)

        
    def addCard(self, img: Image.Image, cardSet: str) -> None:
        self.cardGallery.addImage(img, cardSet)


    def clearCard(self) -> None:
        self.cardGallery.clear()


    def clearArt(self) -> None:
        self.artGallery.clear()
