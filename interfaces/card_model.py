from typing import TypedDict


class Deck(TypedDict):
    onGameId: str
    card_id: str
    card_name: str
    card_image: str
    card_type: str
    card_element: str
    card_attack: int
    card_def: int
    card_cust: int
    card_description: str


class LoadDeckResponse(TypedDict):
    hasDeck: bool
    deck: list[Deck]
