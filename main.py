plansza = []
statki = [4,3,3,2,2,1,1,1,1]
for i in range(10):
    plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])



def add_boat(orient,pos_start,length,plansza):
    zapis_plansza = []
    for i in range(10):
        zapis_plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(10):
        for j in range(10):
            zapis_plansza[i][j] = plansza[i][j]
    #Cały czas wynika jakaś korelacja nawet przy użyciu copy albo list albo czegokolwiek


    for statek in statki:
        #print(statek,length)
        if statek == length:
            
            if orient:
                for i in range(length):
                    pos_x,pos_y = [pos_start[0]+i,pos_start[1]]
                    #print(pos_x,pos_y)
                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                        if plansza[pos_x][pos_y] == 0:
                            plansza[pos_x][pos_y] = 1
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
                                plansza[pos_x][pos_y] = 2

                        for j in range(length+2):
                            pos_x,pos_y = [pos_start[0]+j-1,pos_start[1]-1]
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                plansza[pos_x][pos_y] = 2


                        for j in range(length+2):
                            pos_x,pos_y = [pos_start[0]+j-1,pos_start[1]]
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                if plansza[pos_x][pos_y] == 0:
                                    plansza[pos_x][pos_y] = 2
                        statki.remove(length)
                        return plansza

            else:
                for i in range(length):
                    pos_x,pos_y = [pos_start[0],pos_start[1]+i]
                    #print(pos_x,pos_y)
                    if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9 :
                        if plansza[pos_x][pos_y] == 0:
                            plansza[pos_x][pos_y] = 1
                        print("dodano")
                    else:
                        print("błąd nie udało się dodać nie ma miejsca")
                        return zapis_plansza
                    if i == length-1:
                        for j in range(length+2):
                            pos_x,pos_y = [pos_start[0]-1,pos_start[1]-1+j]
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                plansza[pos_x][pos_y] = 2

                        for j in range(length+2):
                            pos_x,pos_y = [pos_start[0]+1,pos_start[1]-1+j]
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                plansza[pos_x][pos_y] = 2


                        for j in range(length+2):
                            pos_x,pos_y = [pos_start[0],pos_start[1]-1+j]
                            if pos_x >= 0 and pos_x <= 9 and pos_y >= 0 and pos_y <= 9:
                                if plansza[pos_x][pos_y] == 0:
                                    plansza[pos_x][pos_y] = 2
                        statki.remove(length)
                        return plansza
    print("Nie ma już takiego statku do postawnienia")    
    return zapis_plansza




#orient False dla pionowego   True dla poziomego

plansza = add_boat(True,[3,3],4,plansza) 
print(statki)
#plansza = add_boat(True,[4,4],3,plansza) 
#print(statki)
#plansza = add_boat(False,[0,3],4,plansza) 

for i in range(10):
    print(plansza[i])

