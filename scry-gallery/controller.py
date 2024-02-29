from typing import List

from ui.appframe import AppFrame
from resourcemanager import ResourceManager, DATABASE_PATH
from card import Card, ImageType
from carditerators import UniqueArtistIterator, ArtistIterator
from carddb import CardDataBase


class Controller:
    def __init__(self, app: AppFrame) -> None:
        self._app = app
        self._resourceManager = ResourceManager()
        self._resourceManager.ensureDataBase()
        self._cardDB = CardDataBase(DATABASE_PATH)
        self._cardNames: List[str] = []
        self._cardVariations: List[Card] = []

        self._app.startBtn.configure(command=self.run)
        self._app.onCardClick(self._clickedCard)
        self._app.onArtClick(self._clickedArt)


    def _clickedArt(self) -> None:
        # get artist name
        artist = self._app.getClickedArtist()
        self._app.setStatus(f"Selected art by f{artist}")
        # load cards from artist
        self._app.clearCard()
        self._loadCardGallery(self._cardVariations, artist)


    def _clickedCard(self) -> None:
        # write image to disk
        card = self._app.getClickedCard()
        self._app.setStatus(f"Writing {card[1]}")
        self._app.update()
        self._resourceManager.writeImg(card[0], card[1])

        # clear galleries
        self._app.clearArt()
        self._app.clearCard()

        # run the next card
        if len(self._cardNames) > 0:
            self.runCard(self._cardNames.pop())
        else:
            self._app.setStatus("Finished")


    def _loadArtGallery(self, cards: List[Card]) -> None:
        self._app.setStatus(f"Loading Arts for {cards[0].cardname}, this could take a while")
        self._app.update()
        for card in UniqueArtistIterator(cards):
            img = self._resourceManager.requestImage(card.getImgUri(ImageType.ART_CROP))
            self._app.addArt(img, card.artist)
            self._resourceManager.dutySleep()
        self._app.setStatus(f"Loaded Arts for {cards[0].cardname}")
        self._app.update()


    def _loadCardGallery(self, cards: List[Card], artist: str) -> None:
        self._app.setStatus(f"Loading {cards[0].cardname} by {artist}, this could take a while")
        self._app.update()
        for card in ArtistIterator(cards, artist):
            img = self._resourceManager.requestImage(card.getImgUri(ImageType.PNG))
            self._app.addCard(img, card.getId())
            self._resourceManager.dutySleep()
        self._app.setStatus(f"Loaded {cards[0].cardname} by {artist}")
        self._app.update()


    def extractName(self, inStr: str) -> str:
        # Format for cards is /\dx \w+/: NUMBERx CARDNAME
        return inStr[inStr.find('x')+1:].strip()


    def runCard(self, cardName: str) -> None:
        self._app.setStatus(f"{cardName} ({len(self._cardNames)} cards left)")
        self._app.setCardName(cardName)
        self._app.update()
        self._cardVariations = self._cardDB.fetchCards(cardName)
        if len(self._cardVariations) == 0:
            print(f"Couldn't find {cardName}, skipping")
            if len(self._cardNames) > 0:
                self.runCard(self._cardNames.pop())
                return
            else:
                self._app.setStatus("Finished")
                return

        self._loadArtGallery(self._cardVariations)


    def run(self) -> None:
        self._app.clearArt()
        self._app.clearCard()
        cardTxt = self._app.textField.get('1.0', 'end')
        self._cardNames = [self.extractName(card) for card in cardTxt.splitlines()]
        if len(self._cardNames) >= 0:
            self.runCard(self._cardNames.pop())

