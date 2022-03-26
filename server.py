import socket
import threading

HEADER = 64
PORT = 9879
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

class connection:
    def __init__(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        self.addr = addr
        self.conn = conn
        self.mod = 0
        self.connect = True
    def start_lissining(self):
        
        def message_in():
            msg_length = self.conn.recv(HEADER).decode(FORMAT)
            
            if msg_length:
                msg_length = int(msg_length)
                msg = self.conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    self.connect = False
                print(f"[{self.addr}] {msg}")
                Accept = "ACCEPTED"
                self.conn.send(Accept.encode(FORMAT))


        while self.connect:
            if self.mod == 0:
                message_in()
            
        self.conn.close()
        print(f"[DISCONNECTED] {self.addr} DISCONNECTED")

    


def handle_client(conn, addr):
    
    C1 = connection(conn,addr)
    C1.start_lissining()
    
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}" )

print("[STARTING] server is starting... ")
start()