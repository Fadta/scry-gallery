from __future__ import annotations
from enum import Enum

class ImageType(Enum):
    SMALL='small'
    NORMAL='normal'
    LARGE='large'
    PNG='png'
    ART_CROP='art_crop'
    BORDER_CROP='border_crop'


class Card:
    def __init__(self, cardname: str, artist: str, cardSet: str, artId: str, imgs_uri: dict) -> None:
        self.cardname = cardname
        self.artist = artist
        self.artId = artId
        self.cardSet = cardSet
        self.imgs_uri = imgs_uri


    def getId(self) -> str:
        return f"CARD__{self.cardSet}_{self.cardname}_{self.artist}"

    
    def getImgUri(self, img: ImageType) -> str:
        return self.imgs_uri[img.value]
        

    @staticmethod
    def dict2card(data: dict) -> Card:
        keys = data.keys()
        cardname = data['name']
        artId = data['illustration_id'] if 'illustration_id' in keys else 'unknown'
        artist = data['artist']
        cardSet = data['set']
        imgs_uri = data['image_uris'] if 'image_uris' in keys else {}
        return Card(cardname, artist, cardSet, artId, imgs_uri)
