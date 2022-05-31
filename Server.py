from asyncio.windows_events import NULL
from logging import NullHandler
import socket
from sqlite3 import connect 
import threading
import pickle

#from WEB_Socket.main import add_boat

#Zrobić activiti register

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname("192.168.0.165")
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
user_limit = 32
users = {}
for i in range(user_limit + 1): #AKCeEPTACJA 32 uzytkowników
    users[str(i)] = 0

tables = {}
table_limits = int((user_limit/2) +1)
for i in range(table_limits): #Tworzenie stołów 
    tables[str(i)] = 0


class Table():
    def __init__(self,user):
        self.user_1 = user
        self.user_2 = NULL
        self.full = False
        for table in tables:
            if tables[table] == 0:
                self.id = table 
                self.user_1.conn.send("Table created Succesfull".encode(FORMAT))
                print("[Table created Succesfull]")
                return  
    def join_and_play(self,user):
        self.user_2 = user
        self.full = True
        self.user_2.conn.send("Table joined Succesfull".encode(FORMAT))
        print("[Table joined Succesfull Game Start]")
        self.user_1.conn.send("Gra zaczyna się właśnie teraz User1".encode(FORMAT))
        self.user_2.conn.send("Gra zaczyna się właśnie teraz User2".encode(FORMAT))
    
        self.user_1.conn.send("Możesz wysłać statki".encode(FORMAT))
        self.user_2.conn.send("Możesz wysłać statki".encode(FORMAT))
        
        #Przypisanie statków do postawienia 
        self.user_1.statki = [4,3,3,2,2,1,1,1,1]
        self.user_2.statki = [4,3,3,2,2,1,1,1,1]

        #Przypisanie Planszy 
        self.user_1.plansza = []
        for i in range(10):
           self.user_1.plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.user_2.plansza = []
        for i in range(10):
           self.user_2.plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
         


    def disconect(self,user):
        print("Disconected from table")
        if self.user_1 == user:
            print("[User1] Disconected from table")
            self.user_2.conn.send("!DISCONNECT".encode(FORMAT))
            self.user_2.connect_game = False
        else:
            print("[User2] Disconected from table")
            self.user_1.conn.send("!DISCONNECT".encode(FORMAT))
            self.user_1.connect_game = False

    



    #Funkcja dodowania łudki do planszy przyjmuje orientacje i punkt zaczynający się statku i statek, Sprawdza czy dany statek może być w danym miejscu 

class Client():
    def __init__(self,conn,addr):
        self.addr = addr
        self.conn = conn
        self.id = NULL
        self.connect_game = True    

    def login(self):
        connected = True
        while connected:
            msg = self.conn.recv(2048)
            try:
                recd = pickle.loads(msg)
            except:
                print("[Użytkownik sie wyjebał na pysk]")
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                break
            if recd["acctiviti"] == DISCONNECT_MESSAGE:
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                self.conn.send("Connection succesfull closed :) ".encode(FORMAT))
            if recd["acctiviti"] == "PRINT":
                print(self.addr, self.id, recd["content"])
                self.conn.send("Msg received".encode(FORMAT))
            if recd["acctiviti"] == "LOGIN":
                print(recd["login"])
                print(recd["password"])
                if recd["login"] == "test123":
                    self.conn.send("True".encode(FORMAT))
                    for user in users:
                        if users[user] == 0:
                            self.id = user
                            return True

                else:
                    self.conn.send("False".encode(FORMAT))
            
        self.conn.close()
        return False


    def waitning(self):
        print("[Wainting]", self.addr)
        connected = True
        while connected:
            msg = self.conn.recv(2048)
            try:
                recd = pickle.loads(msg)
            except:
                print("[Użytkownik sie wyjebał na pysk]")
                connected = False
                print("[CONNECTION CLOSED]", self.addr)
                self.conn.close()
                users[self.id] = 0
                self.connect_game = False
                break
            if recd["acctiviti"] == "TABLE":
                for table in tables:
                    if tables[table] != 0:
                        if tables[table].full == False:
                            tables[table].join_and_play(users[self.id])
                            self.table = tables[table]
                            connected = False
                            print("breake", self.addr)
                            break
                    else:
                        tablee = Table(users[self.id])
                        tables[tablee.id] = tablee
                        self.table = tablee
                        connected = False
                        print("breake", self.addr)
                        break
    
    
    def game(self):
        def add_boat(orient,pos_start,length):
            zapis_plansza = []
            for i in range(10):
                zapis_plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            for i in range(10):
                for j in range(10):
                    zapis_plansza[i][j] = self.plansza[i][j]
            #Cały czas wynika jakaś korelacja nawet przy użyciu copy albo list albo czegokolwiek


            for statek in self.statki:
                #print(statek,length)
                if statek == length:
                    
                    if orient:
                        for i in range(length):
                            pos_x,pos_y = [pos_start[0]+i,pos_start[1]]
                            #print(pos_x,pos_y)
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                if self.plansza[pos_x][pos_y] == 0:
                                    self.plansza[pos_x][pos_y] = 1
                                else:
                                    print("nie można postawić tu tego magicznego okrętu")
                                    return zapis_plansza
                                print("dodano")
                            else:
                                print("błąd nie udało się dodać nie ma miejsca")
                                return zapis_plansza
                            if i == length-1:
                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0]+j-1,pos_start[1]+1]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        self.plansza[pos_x][pos_y] = 2

                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0]+j-1,pos_start[1]-1]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        self.plansza[pos_x][pos_y] = 2


                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0]+j-1,pos_start[1]]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        if self.plansza[pos_x][pos_y] == 0:
                                            self.plansza[pos_x][pos_y] = 2
                                self.statki.remove(length)
                                return self.plansza

                    else:
                        for i in range(length):
                            pos_x,pos_y = [pos_start[0],pos_start[1]+i]
                            #print(pos_x,pos_y)
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9 :
                                if self.plansza[pos_x][pos_y] == 0:
                                    self.plansza[pos_x][pos_y] = 1
                                print("dodano")
                            else:
                                print("błąd nie udało się dodać nie ma miejsca")
                                return zapis_plansza
                            if i == length-1:
                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0]-1,pos_start[1]-1+j]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        self.plansza[pos_x][pos_y] = 2

                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0]+1,pos_start[1]-1+j]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        self.plansza[pos_x][pos_y] = 2


                                for j in range(length+2):
                                    pos_x,pos_y = [pos_start[0],pos_start[1]-1+j]
                                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                        if self.plansza[pos_x][pos_y] == 0:
                                            self.plansza[pos_x][pos_y] = 2
                                self.statki.remove(length)
                                return self.plansza
            print("Nie ma już takiego statku do postawnienia")    
            return zapis_plansza

        
        print("[Game Start]", self.addr)
        self.connect_game = True
        while self.connect_game:
            msg = self.conn.recv(2048)
            recd = pickle.loads(msg)
            

            if recd["acctiviti"] == "MESSAGE":
                print(f"[Table id {self.table.id}] Message: " + recd['CONTENT'] ) #Message beetwen 2 users
                if self.table.user_1.id == self.id:
                    print("tu")
                    self.table.user_2.conn.send(recd["CONTENT"].encode(FORMAT))
                else:
                    print("tam")
                    self.table.user_1.conn.send(recd["CONTENT"].encode(FORMAT))
            if  recd["acctiviti"] == "STATKI":
                print("Przyjęto statek")
                print(self.statki,self.plansza)
                print(recd["orient"],[recd["pos_x"],recd["pos_y"]],recd["length"])
                self.plansza = add_boat(recd["orient"],[recd["pos_x"],recd["pos_y"]],recd["length"])
                for i in range(10):
                    print(self.plansza[i])
                
                self.conn.send("Dodano".encode(FORMAT))

            if recd["acctiviti"] == "!DISCONNECT":
                print("[]Użytkownik rozłączył sie podczas stołu")
                self.table.disconect(users[self.id])
                self.connect_game = False ###Funkcja w stole która zamkyka go usuwa przypisanych użytkowników od stołu i informuje ich o tym
        print("[]Gra zakończona prawidłowo")

    




def handle_client(conn, addr):
    global users
    print(f"[NEW CONNECTION] {addr} connected.")
    print("[USER ADD]", addr)
    guest =  Client(conn,addr)
    status = guest.login()
    print("status", status)
    if status:
        print("[AUTHENTICATION SUCCESFULL] id:", guest.id)
        users[guest.id] = guest
        #status = 
        guest.waitning()
        while guest.connect_game:
            guest.game()
            
            guest.waitning()
    else:
        print("[AUTHENTICATION FALS]")


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