from __future__ import annotations
from typing import List
from card import Card


class CardIterator:
    def __init__(self, cardList: List[Card]) -> None:
        self._currentIx = 0
        self._cardList = cardList


    def __iter__(self) -> CardIterator:
        self._currentIx = 0
        return self


    def __next__(self) -> Card:
        if self._currentIx >= len(self._cardList):
            raise StopIteration
        currentCard = self._cardList[self._currentIx]
        self._currentIx += 1
        return currentCard


class UniqueArtistIterator(CardIterator):
    def __init__(self, cardList: List[Card]) -> None:
        self._cardList = cardList
        self._currentIx = 0
        self._seenArtists: List[str] = []

    
    def __iter__(self) -> UniqueArtistIterator:
        self._currentIx = 0
        self._seenArtists = []
        return self


    def __next__(self) -> Card:
        if self._currentIx >= len(self._cardList):
            raise StopIteration

        while self._cardList[self._currentIx].artist in self._seenArtists:
            self._currentIx += 1
            if self._currentIx >= len(self._cardList):
                raise StopIteration

        self._seenArtists.append(self._cardList[self._currentIx].artist)

        currentCard = self._cardList[self._currentIx]
        self._currentIx += 1
        return currentCard


class ArtistIterator(CardIterator):
    def __init__(self, cardList: List[Card], artist:str):
        self._cardList = cardList
        self._currentIx = 0
        self._artist = artist

    def __iter__(self) -> ArtistIterator:
        self._currentIx = 0
        return self


    def __next__(self) -> Card:
        if self._currentIx >= len(self._cardList):
            raise StopIteration

        while self._cardList[self._currentIx].artist != self._artist:
            self._currentIx += 1
            if self._currentIx >= len(self._cardList):
                raise StopIteration

        currentCard = self._cardList[self._currentIx]
        self._currentIx += 1
        return currentCard
