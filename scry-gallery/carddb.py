import json
from card import Card

class CardDataBase:
    def __init__(self, dbPath: str) -> None:
        self.cards = None
        self.lastFetch = []

        print("Loading Cards")
        with open(dbPath) as cards:
            self.cards = json.load(cards)
        print("Cards Loaded")
        
    def fetchCards(self, cardName: str) -> list[Card]:
        if self.cards is None:
            self.lastFetch = []
            print("No DB Loaded")
            return self.lastFetch

        cardList = []
        for card in self.cards:
            if card["name"] == cardName:
                cardList.append(Card.dict2card(card))

        self.lastFetch = cardList
        return self.lastFetch


    def getLastFetch(self):
        return self.lastFetch


    def __getitem__(self, cardName: str):
        return self.fetchCards(cardName)
