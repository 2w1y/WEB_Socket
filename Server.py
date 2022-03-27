import socket 
import threading
import pickle



HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
users = {}
for i in range(33): #AKCeEPTACJA 32 uzytkowników
    users[str(i)] = 0

class Client():
    def __init__(self,conn,addr,idd):
        self.addr = addr
        self.conn = conn
        self.id = idd
    def start(self):
        connected = True
        while connected:
            msg = self.conn.recv(2048)
            recd = pickle.loads(msg)
            if recd["acctiviti"] == DISCONNECT_MESSAGE:
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
            if recd["acctiviti"] == "PRINT":
                print(self.addr, self.id, recd["content"])
            self.conn.send("Msg received".encode(FORMAT))

        self.conn.close()





def handle_client(conn, addr):
    global users
    print(f"[NEW CONNECTION] {addr} connected.")
    for user in users:
        if users[user] == 0:
            print("[USER ADD] ID:", user)
            users[user] = Client(conn,addr,user)
            users[user].start()
            print("[USER DELLETED] ID:", user)
            users[user] = 0
        #users.append()
    
        

def start():
    server.listen(32)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()