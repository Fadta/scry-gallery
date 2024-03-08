import os
import os.path
import requests
import time
from PIL import Image


SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(SCRIPT_DIRECTORY, 'scryfall.json')

class ResourceManager:
    def __init__(self):
        self._outputFolder = os.path.join(SCRIPT_DIRECTORY, 'output')
        self.API_CITIZENSHIP_DELAY = 0.06


    # TODO
    def ensureDataBase(self) -> None:
        pass


    def _fetchDataBase(self) -> None:
        pass


    def ensureOutputFolder(self) -> None:
        if not os.path.exists(self._outputFolder):
            os.makedirs(self._outputFolder)
        else:
            if not os.path.isdir(self._outputFolder):
                os.makedirs(self._outputFolder)


    def writeImg(self, img: Image.Image, name: str) -> None:
        self.ensureOutputFolder()
        img.save(os.path.join(self._outputFolder, name+'.png'))


    def requestImage(self, imageURI: str) -> Image.Image:
        img = Image.open(requests.get(imageURI, stream=True).raw)
        return img

    
    def dutySleep(self) -> None:
        time.sleep(self.API_CITIZENSHIP_DELAY)
