from math import sqrt
from math import atan2
from math import pi
import numpy as np

def angle_between(destination_x, origin_x, destination_y, origin_y):
    deltaX = destination_x - origin_x
    deltaY = destination_y - origin_y
    degrees_temp = atan2(deltaX, deltaY)/pi*180

    degrees_temp = degrees_temp + 180

    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp
    degrees_final = degrees_final - 360
    degrees_final = degrees_final * -1
    return degrees_final

def distance(a,b):
    return sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def is_between(a,b,c):
    return distance(a,c) + distance(c,b) == distance(a,b)

def isBetween(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) != 0:#epsilon:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True

class point(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

class asteroid(object):
    def __init__(self,col,row):
        self.x = row
        self.y = col
        self.count = 0
        self.distance_from_base = 0
        self.angle_from_base = 0
    def __str__(self):
        return str(self.x)+","+str(self.y)
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def loc(self):
        return (self.x,self.y)


#inputfile = "day10_test7.txt"
inputfile = "day10_input.txt"

f = open(inputfile)

lines = f.read().splitlines()

chart = []

asteroids = []

row = 0
for l in lines:
    points = list(l)
    #print(row,points)
    row = row + 1
    chart.append(points)

for c in range(len(chart)):
    for r in range(len(points)):
        #print(chart[r][c])
        if chart[c][r] == '#':
            asteroids.append(asteroid(c,r))

#print(asteroids)

for r1 in asteroids:
    
    for r2 in asteroids:
        clear = True    
        if r1.loc != r2.loc:
            
            for r3 in asteroids:
                if r3.loc != r1.loc and r3.loc != r2.loc:
                    if isBetween(r1,r2,r3) == True:
                        #print(r1," view of ",r2, " blocked by ", r3)
                        clear = False
                        break

            if clear == True:
                #print(r1," has view of ",r2)
                r1.count = r1.count + 1
            


maxans = 0
locations = []
print(len(asteroids),"asteroids")
for r in asteroids:
    print(r,r.count)
    locations.append(r.loc())                
    if r.count > maxans:
        maxans = r.count

print("highest number seen: ",maxans)

#base = (8,3)
base = (22,25)

for y in range(len(lines)):
    line = ""
    for x in range(len(lines[0])):
        if (x,y) == base:
            line = line + 'X'
        elif (x,y) in locations:
            line = line + '#'
        else:
            line = line + '.'
    print(line)

for a in asteroids:
    a.distance_from_base = distance(point(a.getX(),a.getY()),point(base[0],base[1]))           
    a.angle_from_base = angle_between(a.getX(),base[0],a.getY(),base[1])      

print(len(asteroids))
asteroids.sort(key=lambda x: (x.angle_from_base, x.distance_from_base))
blasted = []

for a in asteroids:
    if a.loc() not in blasted:
        #print(a,a.angle_from_base,a.distance_from_base)
        target = a
        for a2 in asteroids:
            if a2.angle_from_base == target.angle_from_base and a2.distance_from_base < target.distance_from_base and a2 not in blasted:
                target = a2
        if target.loc() not in blasted:
            print(len(blasted)+1, " blasted ", target.loc())
            blasted.append(target.loc())
print("blasted ", len(blasted),"of",len(asteroids))
    
for b in blasted:
    for i,o in enumerate(asteroids):
        if o.loc() == b:
            del asteroids[i]
            #print(o.loc(),b)
            break

#for a in asteroids:
    #print(a)

for a in asteroids:
    if a.loc() not in blasted:
        #print(a,a.angle_from_base,a.distance_from_base)
        target = a
        for a2 in asteroids:
            if a2.angle_from_base == target.angle_from_base and a2.distance_from_base < target.distance_from_base and a2 not in blasted:
                target = a2
        if target.loc() not in blasted:
            print(len(blasted)+1, " blasted ", target.loc())
            blasted.append(target.loc())
