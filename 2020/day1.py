file1 = open('day1_input.txt', 'r') 
lines = file1.readlines() 

for l1 in lines:
    for l2 in lines:
        for l3 in lines:  
            a = int(l1.strip())
            b = int(l2.strip())
            c = int(l3.strip())
            if a+b+c == 2020 and a != b != c:
                print(f"{a} + {b} + {c} = {a+b+c} {a*b*c}")