import itertools
from math import gcd

class planet(object):
    def __init__(self,name,x,y,z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0
    
    def __str__(self):
        return self.name+": pos=<x="+str(self.x)+", y="+str(self.y)+", z="+str(self.z)+">, vel=<x="+str(self.vx)+", y="+str(self.vy)+", z="+str(self.vz)+"> "+str(self.calc_energy())

    def calc_energy(self):
        return (abs(self.x)+abs(self.y)+abs(self.z))*(abs(self.vx)+abs(self.vy)+abs(self.vz))
    
    

#europa = planet("Europa",1,2,3)
#print(europa)

system = []

#system.append(planet("p1",-1,0,2))
#system.append(planet("p2",2,-10,-7))
#system.append(planet("p3",4,-8,8))
#system.append(planet("p4",3,5,-1))

#system.append(planet("p1",-8,-10,0))
#system.append(planet("p2",5,5,10))
#system.append(planet("p3",2,-7,3))
#system.append(planet("p4",9,-8,-3))

system.append(planet("p1",3,2,-6))
system.append(planet("p2",-13,18,10))
system.append(planet("p3",-8,-1,13))
system.append(planet("p4",5,10,4))

step = 0
total_energy = -1
x_p = None
y_p = None
z_p = None

while (total_energy != 0):
    step = step + 1
    for p1,p2 in itertools.combinations(system,2):
        if p1.name != p2.name:
            #print("comparing",p1.name,p2.name)
            if p1.x > p2.x:
                p1.vx = p1.vx - 1
                p2.vx = p2.vx + 1
            elif p1.x < p2.x:
                p1.vx = p1.vx + 1
                p2.vx = p2.vx - 1
            
            if p1.y > p2.y:
                p1.vy = p1.vy - 1
                p2.vy = p2.vy + 1
            elif p1.y < p2.y:
                p1.vy = p1.vy + 1
                p2.vy = p2.vy - 1

            if p1.z > p2.z:
                p1.vz = p1.vz - 1
                p2.vz = p2.vz + 1
            elif p1.z < p2.z:
                p1.vz = p1.vz + 1
                p2.vz = p2.vz - 1

    for p in system:
        p.x = p.x + p.vx
        p.y = p.y + p.vy
        p.z = p.z + p.vz

    total_energy = 0
    x_energy = 0
    y_energy = 0
    z_energy = 0

    #if step%100000==0:
    #    print("step:",step)
    for p in system:
        #print(p)
        total_energy = total_energy + p.calc_energy()
        x_energy = x_energy + abs(p.vx)
        y_energy = y_energy + abs(p.vy)
        z_energy = z_energy + abs(p.vz)
    
    if x_energy == 0 and x_p == None:
        print("vx=0 at step:",step)
        if x_p == None:
            x_p = step
    if y_energy == 0 and y_p == None:
        print("vy=0 at step:",step)
        if y_p == None:
            y_p = step
    if z_energy == 0 and z_p == None:
        print("vz=0 at step:",step)
        if z_p == None:
            z_p = step

    if x_p != None and y_p != None and z_p != None:
        a = [x_p, y_p, z_p]
        lcm = a[0]
        for i in a[1:]:
            lcm = lcm*i//gcd(lcm,i)
        print(lcm*2)
        break
    #print(step,total_energy,x_p,y_p,z_p)
#for p in system:
    #print(p)
    