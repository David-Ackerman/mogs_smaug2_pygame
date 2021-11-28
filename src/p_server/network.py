import socket
import pickle

d = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
d.connect(("8.8.8.8", 80))
ip = d.getsockname()[0]
d.close()

hostname = socket.gethostname()
local_ip = ip


class Network:
    def __init__(self, userName: str, ip: str = ""):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(local_ip)
        self.server = local_ip if ip == "" else ip
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
            return pickle.loads(self.client.recv(12288))
        except Exception as e:
            print("Error: ", str(e))
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(12288))
        except Exception as e:
            print(e)
