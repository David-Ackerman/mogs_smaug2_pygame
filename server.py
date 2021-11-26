import pickle
import socket
from _thread import *
from src.server.duel import Duel
from src.server.combat import Combat

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

server = local_ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(4)
print("Waiting for a connection, server started")

connected = set()
combats = {}
duels = {}
idCount = 0


def threaded_client(conn, p, gameId: int):
    global idCount

    conn.send(pickle.dumps({
        'player': p
    }))
    while True:
        try:
            data = pickle.loads(conn.recv(8192))
            if gameId in duels and gameId in combats:
                game: Duel = duels[gameId]
                combat: Combat = combats[gameId]
                combat.game = game
                if not data:
                    break
                if data['action'] == 'quit':
                    break
                elif data['action'] == "get":
                    combat.setPlayerCards(data['player'], data['cards'])
                elif data['action'] == "selectEnemyCard":
                    combat.selectEnemyCard(
                        data['player'], data['selectedCard'])
                elif data['action'] == "directAttack":
                    combat.combat(data['player'], data['attacking'])
                elif data['action'] == "combat":
                    combat.combat(data['player'],
                                  data['attacking'], data['defending'])
                elif data['action'] == "summon":
                    combat.summonCard(data['player'], data['summoned'], )
                elif data['action'] == "drawCard":
                    combat.changeTurn()
                    combat.setPlayerCards(data['player'], data['cards'])
                elif data['action'] == "changePlayerTime":
                    combat.changePlayerTime()
                    combat.setPlayerCards(data['player'], data['cards'])
                elif data['action'] == "battlePhase":
                    combat.setBattlePhase()
                    combat.setPlayerCards(data['player'], data['cards'])

                conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as e:
            print('exception', e)
            break

    print("Lost Connection!!")
    try:
        del duels[gameId]
        del combats[gameId]
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
        duels[gameId] = Duel(gameId, p)
        data = pickle.loads(conn.recv(8192))
        duels[gameId].players[data['username'] + str(p)] = {'mana': 14,
                                                            'life': 200,
                                                            'cards': {
                                                                'hand': [],
                                                                'deck': [],
                                                                'field': {
                                                                    'front': [],
                                                                    'support': []
                                                                },
                                                                'grave': [],
                                                            }}
        combats[gameId] = Combat(gameId, duels[gameId])
        print("Creating a new game...")
    else:
        p = 1
        duels[gameId].ready = True
        duels[gameId].duelInit = True
        duels[gameId].turn = 1
        duels[gameId].players[data['username'] + str(p)] = {
            'mana': 14,
            'life': 200,
            'cards': {
                'hand': [],
                'deck': [],
                'field': {
                    'front': [],
                    'support': []
                },
                'grave': [],
            }}
        combats[gameId].ready = True

    start_new_thread(threaded_client, (conn, p, gameId))
