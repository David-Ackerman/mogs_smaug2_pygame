import pickle
import socket
from _thread import *
from duel import Duel

server = "192.168.0.177"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, server started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId: int):
    global idCount

    # conn.send(str.encode(str(p)))
    conn.send(pickle.dumps({
        'player': p
    }))
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if gameId in games:
                game: Duel = games[gameId]
                if not data:
                    break
                else:
                    if data['action'] == "get":
                        game.setPlayerCards(data['player'], data['cards'])
                    elif data['action'] == "drawCard":
                        game.changeTurn()
                        game.setPlayerCards(data['player'], data['cards'])
                    elif data['action'] == "changePlayerTime":
                        game.changePlayerTime()
                        game.setPlayerCards(data['player'], data['cards'])

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print(e)
            break

    print("Lost Connection!!")
    try:
        del games[gameId]
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    conn.settimeout(60)
    if idCount % 2 == 1:
        games[gameId] = Duel(gameId, p)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        games[gameId].duelInit = True
        games[gameId].turn = 1
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
