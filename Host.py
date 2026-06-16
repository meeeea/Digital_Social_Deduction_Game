import socket
from select import select

import pygame


def main():
    HOST = "0.0.0.0"                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Master_Socket:
        Master_Socket.bind((HOST, PORT))
        Master_Socket.listen(1)
        
        print("Server launched at: ", Master_Socket.getsockname())

        SERVER_ON = True
        Players = []
        while SERVER_ON:
            read, [], [] = select(Players + [Master_Socket], [], [], 0.5)
            for connection in read:
                if connection == Master_Socket:
                    conn, addr = Master_Socket.accept()
                    Players.append(conn)
                    print(addr)
                else:
                    if data := connection.recv(1024):
                        for Player in Players:
                            Player.sendall(data)

                    else:
                        print(f"Lost connection with {connection.getpeername()}")
                        connection.close()
                        Players.remove(connection)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't need to be a reachable or live target address
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

if __name__ == "__main__":
    main()