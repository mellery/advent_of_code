filename = "input22.txt"
#filename = "input22_ex1.txt"
#filename = "input22_ex2.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

p1deck = []
p2deck = []

p1found = False
p2found = False

def calc_score(deck):
    size = len(deck)
    score = 0
    for c in deck:
        score = score + c*size
        size = size - 1
    return score

subgames = []

def play_round(d1,d2, depth):
    #print('P1 deck',d1)
    #print('P2 deck',d2)
    #print('P1 plays',d1[0])
    #print('P2 plays',d2[0])

    if len(d1)-1 >= d1[0] and len(d2)-1 >= d2[0]:
        #print("playing sub-game to determine the winner...")
        subgame = True
        subround = 0
        gamedepth = depth+1
        games.append([])
        
        temp1 = d1[1:d1[0]+1].copy()
        temp2 = d2[1:d2[0]+1].copy()
        
        #shortcut
        maxp1 = max(temp1)
        maxp2 = max(temp2)
        if maxp1 > maxp2:
            temp2 = []

        while len(temp1) > 0 and len(temp2) > 0 and subgame == True:
            subround = subround + 1
            #print("\nsubround",subround, 'subgame', depth)
            subgame, temp1, temp2 = play_round(temp1.copy(),temp2.copy(), gamedepth)

        if len(temp1) > 0:
            d1.append(d1[0])
            d1.append(d2[0])
            d1.pop(0)
            d2.pop(0)

        else:
            d2.append(d2[0])
            d2.append(d1[0])
            d1.pop(0)
            d2.pop(0)

        result = (calc_score(d1),calc_score(d2))

        if result not in games[depth]:
            games[depth].append(result)
        else:
            print("subgamestop!")
            games[depth] = []
            return False, d1.copy(), d2.copy()

        return True, d1.copy(), d2.copy()

    else:

        if d1[0] > d2[0]:            
            d1.append(d1[0])
            d1.append(d2[0])
            d1.pop(0)
            d2.pop(0)

        elif d2[0] > d1[0]:
            d2.append(d2[0])
            d2.append(d1[0])
            d1.pop(0)
            d2.pop(0)

        result = (calc_score(d1),calc_score(d2))
        if result not in games[depth]:
            games[depth].append(result)
        else:
            return False, d1.copy(), d2.copy()

        return True, d1.copy(), d2.copy()

for l in lines:
    temp = l.strip()
    if temp == '\n':
        continue
    elif 'Player 1' in temp:
        p1found = True
    elif p1found == True and p2found == False:
        
        if 'Player 2' in temp:
            p2found = True
        elif temp.isdigit():
            p1deck.append(int(temp))  

    elif temp.isdigit():
        p2deck.append(int(temp))

round = 0
run = True
games = []
games.append([])
while len(p1deck) > 0 and len(p2deck) > 0 and run == True:

    round = round + 1
    print("\n---Round",round,"---")

    run, p1deck, p2deck = play_round(p1deck.copy(),p2deck.copy(), 0)


print("--Post game results")
print("P1",p1deck)
print("P2",p2deck)

print("P1",calc_score(p1deck))
print("P2",calc_score(p2deck))

#14051 too low
#want 36246