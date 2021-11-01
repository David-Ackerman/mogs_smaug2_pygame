from typing import TypedDict

class Deck(TypedDict):
    card_id: str
    name: str
    imageName: str
    text: str
    card_type: str
    card_power: int

class LoadDeckResponse(TypedDict):
    hasDeck: bool
    deck: list[Deck]