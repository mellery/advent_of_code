filename = "day5_input.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 

def find_seat(bp):
    rows = 128
    rows_left = []
    cols = 8
    cols_left = []

    

    for x in range(0,rows):
        rows_left.append(x)
    for x in range(0,cols):
        cols_left.append(x)

    #print("range is ",rows_left)
    for x in range(0,7):
        if bp[x] == 'F':
            rows_left = rows_left[:len(rows_left)//2]
        if bp[x] == 'B':
            rows_left = rows_left[len(rows_left)//2:]
        #print(bp[x], rows_left)
    
    

    for x in range(7,10):
        if bp[x] == 'L':
            cols_left = cols_left[:len(cols_left)//2]
        if bp[x] == 'R':
            cols_left = cols_left[len(cols_left)//2:]
        #print(bp[x], cols_left)

    my_row = rows_left[0]
    my_col = cols_left[0]

    bp_value = my_row*8+my_col
    #print("bp: row=",my_row," col=",my_col," val=",bp_value)

    return bp_value

#print(find_seat("FBFBBFFRLR"))

#print(find_seat("BFFFBBFRRR"))
#print(find_seat("FFFBBBFRRR"))
#print(find_seat("BBFFBBFRLL"))

bp_seats = []
bp_max = 0
for l in lines:
    temp = find_seat(l)
    bp_seats.append(temp)
    if temp > bp_max:
        bp_max = temp
print(bp_max)

all_seats = []

for r in range(0,128):
    for c in range(0,8):
        all_seats.append(r*8+c)

#print(len(all_seats))
for l in lines:
    temp = find_seat(l)
    all_seats.remove(temp)

#print(len(all_seats))

#print("===")
for s in all_seats:
    if s+1 in bp_seats and s-1 in bp_seats:
        print(s)
