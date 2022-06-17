from math import floor

def fuelRequired(mass):
    fuel = floor(mass/3)-2
    total = fuel
    print(fuel)
    if fuel <= 0:
        return total
    else:
        while fuel > 0:
            fuel = floor(fuel/3)-2
            print(fuel)
            if fuel > 0:
                total = total + fuel
        return total

    

print('total',fuelRequired(14))
print("---")
print('total',fuelRequired(1969))
print("---")
print('total',fuelRequired(100756))


total = 0

with open('day1_input.txt') as f:
    modules = f.readlines()
    for m in modules:
        total = total + fuelRequired(int(m))

print(total)