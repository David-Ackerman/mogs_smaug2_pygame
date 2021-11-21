import numpy as np
import os
from src.interfaces.card_model import Deck, LoadDeckResponse


def saveDeckOnDisk(deck: list[Deck]):
    if os.path.exists("storage/playerDeck.npy"):
        os.remove("storage/playerDeck.npy")
    np.save("storage/playerDeck.npy", deck, allow_pickle=True)
    print("Deck Salvo com sucesso")


def loadDeckOnDisk() -> LoadDeckResponse:
    response: LoadDeckResponse = {"hasDeck": False, "deck": []}
    try:
        returnedArray = np.load("storage/playerDeck.npy", allow_pickle=True)
        for card in returnedArray:
            response["deck"].append(card)
        response["hasDeck"] = True
    except:
        response["hasDeck"] = False

    return response
