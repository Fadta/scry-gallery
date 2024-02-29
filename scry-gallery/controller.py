from typing import List

from ui.appframe import AppFrame
from resourcemanager import ResourceManager, DATABASE_PATH
from card import Card, ImageType
from carditerators import ArtIterator, UniqueArtistIterator, ArtistIterator
from carddb import CardDataBase


class Controller:
    GETTING_CARDNAME = ""
    GETTING_ARTID = ""
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
        artist = self._app.getClickedArt()
        self._app.setStatus(f"Selected art by f{artist}")
        # load cards from artId
        Controller.GETTING_ARTID = artist
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
        cardname = cards[0].cardname
        self._app.setStatus(f"Loading Arts for {cardname}, this could take a while")
        self._app.update()
        for card in UniqueArtistIterator(cards):
            if cardname != Controller.GETTING_CARDNAME:
                break
            img = self._resourceManager.requestImage(card.getImgUri(ImageType.ART_CROP))
            self._app.addArt(img, card.artId)
            self._app.update()
            self._resourceManager.dutySleep()
        self._app.setStatus(f"Loaded Arts for {cards[0].cardname}")
        self._app.update()


    def _loadCardGallery(self, cards: List[Card], artId: str) -> None:
        cardname = cards[0].cardname
        self._app.setStatus(f"Loading arts for {cardname}")
        self._app.update()
        for card in ArtIterator(cards, artId):
            if artId != Controller.GETTING_ARTID:
                break
            img = self._resourceManager.requestImage(card.getImgUri(ImageType.PNG))
            self._app.addCard(img, card.getId())
            self._app.update()
            self._resourceManager.dutySleep()
        self._app.setStatus(f"Loaded arts for {cardname}")
        self._app.update()


    def extractName(self, inStr: str) -> str:
        # Format for cards is /\dx \w+/: NUMBERx CARDNAME
        return inStr[inStr.find('x')+1:].strip()


    def runCard(self, cardName: str) -> None:
        self._app.setStatus(f"{cardName} ({len(self._cardNames)} cards left)")
        self._app.setCardName(cardName)
        self._app.update()
        self._cardVariations = self._cardDB.fetchCards(cardName)
        print(f"Searching {cardName}")
        if len(self._cardVariations) == 0:
            print(f"Couldn't find {cardName}, skipping")
            if len(self._cardNames) > 0:
                self.runCard(self._cardNames.pop())
                return
            else:
                self._app.setStatus("Finished")
                return

        Controller.GETTING_CARDNAME = cardName
        self._loadArtGallery(self._cardVariations)


    def run(self) -> None:
        self._app.clearArt()
        self._app.clearCard()
        cardTxt = self._app.textField.get('1.0', 'end')
        self._cardNames = [self.extractName(card) for card in cardTxt.splitlines()]
        if len(self._cardNames) >= 0:
            self.runCard(self._cardNames.pop())

