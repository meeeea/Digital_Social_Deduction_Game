from Class import Class
import socket

class Player:
    def __init__(self, sock : socket.socket, number : int, Player_Class : Class):
        self.Socket = sock
        self.Number = number
        self.Class  = Player_Class

    def fileno(self):
        return self.Socket.fileno()
    
    def recv(self, timeout):
        return self.Socket.recv(timeout)
    
    def send(self, message):
        return self.Socket.send(message)
    
    def sendall(self, message):
        return self.Socket.sendall(message)
    
    def close(self):
        return self.Socket.close()