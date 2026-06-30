import socket
from datetime import datetime
from select import select

from src.Player import Player
from src.ServerStateMatchine import StateMatchine

def main():
    HOST = "0.0.0.0"                 # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as Master_Socket:
        Master_Socket.bind((HOST, PORT))
        Master_Socket.listen(1)
        
        print("Server launched at: ", Master_Socket.getsockname())

        SERVER_ON = True
        Players = []

        time = datetime.now()

        end_time = int(time.timestamp()) + 10

        send_time = True

        player_number = 1

        while SERVER_ON:
            time = datetime.now()

            if (now := int(time.timestamp())) > end_time:
                end_time = now + 10
                send_time = True

            read, send, [] = select(Players + [Master_Socket], Players, [], 0.5)
            for connection in read:
                if connection == Master_Socket:
                    conn, addr = Master_Socket.accept()
                    Players.append(Player(conn, player_number))

                    player_number += 1
                    conn.sendall(f"time {end_time}".encode())
                    print("Connection Found:", addr)
                else:
                    if d := connection.recv(1024):
                        data = d.decode().split()
                        if data[0] == "message":
                            for player in Players:
                                player.sendall(" ".join(data).encode())

                    else:
                        print(f"Lost connection with {connection.getpeername()}")
                        connection.close()
                        Players.remove(connection)
            if send_time:
                for player in send:
                    player.sendall(f"time {end_time}".encode())
                send_time = False




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