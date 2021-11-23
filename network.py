import socket
import pickle


class Network:
    def __init__(self, userName: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.177"
        self.userName = userName
        self.sendedUser = False
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            if not(self.sendedUser):
                self.client.send(pickle.dumps(
                    {'username': self.userName, 'action': ''}))
                self.sendedUser = True
            return pickle.loads(self.client.recv(8192))
        except Exception as e:
            print("Error: ", str(e))
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(8192))
        except Exception as e:
            print(e)
