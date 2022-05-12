plansza = []
statki = [4,3,3,]
for i in range(10):
    plansza.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])



def add_boat(orient,pos,length):
    if orient:
        for i in range(length):
            plansza[pos[0]+i][pos[1]] = 1
    else:
        for i in range(length):
            plansza[pos[0]][pos[1]+i] = 1


#orient False dla pionowego   True dla poziomego
add_boat(False,[5,5],3) 

for i in range(10):
    print(plansza[i])

