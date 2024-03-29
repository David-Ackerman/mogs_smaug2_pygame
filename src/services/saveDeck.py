import numpy as np
import os
from src.interfaces.card_model import Deck, LoadDeckResponse


def saveDeckOnDisk(deck: list[Deck], userName: str, options):
    if os.path.exists("/mogs/playerData.npy"):
        os.remove("/mogs/playerData.npy")
    if not os.path.exists('/mogs'):
        os.mkdir('/mogs')
    np.save("/mogs/playerData.npy", [{
        "userName": userName,
        "options": options,
        "deck": deck
    }], allow_pickle=True)
    print("Deck Salvo com sucesso")


def loadDeckOnDisk() -> LoadDeckResponse:
    response: LoadDeckResponse = {"hasDeck": False,
                                  "userName": '',  "options": {},  "deck": []}
    try:
        returnData = np.load("/mogs/playerData.npy", allow_pickle=True)
        response["userName"] = returnData[0]["userName"]
        response["options"] = returnData[0]["options"]
        response["deck"] = returnData[0]["deck"].copy()
        response["hasDeck"] = True
    except:
        response["hasDeck"] = False

    return response
