import math

filename = "input12.txt"
#filename = "input12_ex1.txt"
#filename = "input12_ex2.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

mv = []
dist = []

for l in lines:
    temp = l.strip()
    mv.append(temp[0])
    dist.append(int(temp[1:]))

x = 0
y = 0
wp_x = 10
wp_y = 1
if wp_y > 0:
    wp_lat = 'north'
else:
    wp_lat = 'south'
if wp_x < 0:
    wp_lon = 'west'
else:
    wp_lon = 'east'

print("waypoint at ",abs(wp_x),wp_lon,abs(wp_y),wp_lat)

heading = 'E'

#  N
# W E
#  S

#                     L               R
#             N (0,-1)->(-1,0)    (0,-1)->(1,0)
#             E (1,0)->(0,-1)     (1,0)->(0,-1)
#     N       S (0,-1)->(1,0)    (0,-1)->(-1,0)
#    W E      W (-1,0)->(0,-1)   (-1,0)->(0,-1)
#     S
#     . 
     

def rotate_wp(x,y,wp_x,wp_y,turn,deg):
    
    if turn == 'R':
        for r in range(deg//90):
            temp_x = wp_x
            temp_y = wp_y
            wp_x = temp_y
            wp_y = -temp_x
        return wp_x,wp_y
        
    if turn == 'L':
        for r in range(deg//90):
            temp_x = wp_x
            temp_y = wp_y
            wp_x = -temp_y
            wp_y = temp_x
        return wp_x,wp_y
    

def turn_boat(heading,turn,deg):
    print("facing",heading,"turning",turn,deg,"degrees")
    if deg == 270:
        deg = 90
        if turn == 'L':
            turn = 'R'
        elif turn == 'R':
            turn = 'L'

    if deg == 180:
        if heading == 'N':
            return 'S'
        if heading == 'E':
            return 'W'
        if heading == 'S':
            return 'N'
        if heading == 'W':
            return 'E'

    elif deg == 90:
        if heading == 'N':
            if turn == 'L':
                return 'W'
            if turn == 'R':
                return 'E'

        if heading == 'E':
            if turn == 'L':
                return 'N'
            if turn == 'R':
                return 'S'    

        if heading == 'S':
            if turn == 'L':
                return 'E'
            if turn == 'R':
                return 'W'

        if heading == 'W':
            if turn == 'L':
                return 'S'
            if turn == 'R':
                return 'N'
    else:
        print("degree error",deg)

def move(x,y, mv,dist):
    print("moving ",mv, dist)
    if mv == 'N':
        y = y + dist

    if mv == 'E':
        x = x + dist

    if mv == 'S':
        y = y - dist

    if mv == 'W':
        x = x - dist

    return x,y

for i in range(0, len(mv)):
    print(mv[i],dist[i])

    if mv[i] in ['N','E','S','W']:
        #x,y = move(x,y,mv[i],dist[i])    
        wp_x,wp_y = move(wp_x,wp_y, mv[i],dist[i])

    if mv[i] in ['L','R']:
        #heading = turn_boat(heading,mv[i],dist[i])
        wp_x,wp_y = rotate_wp(x,y,wp_x,wp_y,mv[i],dist[i])
        
    if mv[i] == 'F':
        #x,y = move(x,y,heading,dist[i])
        times = dist[i]
        x = x + (wp_x*times)
        y = y + (wp_y*times)

    if y > 0:
        lat = 'north'
    else:
        lat = 'south'
    if x < 0:
        lon = 'west'
    else:
        lon = 'east'
    
    if wp_y > 0:
        wp_lat = 'north'
    else:
        wp_lat = 'south'
    if wp_x < 0:
        wp_lon = 'west'
    else:
        wp_lon = 'east'

    print("boat at ",abs(x),lon,',',abs(y),lat,"hdg",heading)
    print("wp at",abs(wp_x),wp_lon,",",abs(wp_y),wp_lat,"of boat")

print(abs(x)+abs(y))
#64127 too high
#37083 too low