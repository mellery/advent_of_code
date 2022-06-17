from math import floor

def fuelRequired(mass):
    return floor(mass/3)-2

total = 0

with open('day1_input.txt') as f:
    modules = f.readlines()
    for m in modules:
        total = total + fuelRequired(int(m))

print(total)