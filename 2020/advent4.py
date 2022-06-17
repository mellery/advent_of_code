filename = "input4.txt"
file1 = open(filename, 'r') 
lines = file1.readlines() 

#byr (Birth Year) - four digits; at least 1920 and at most 2002.
def byr_valid(v):
    year = int(v)
    if year >= 1920 and year <= 2002:
        return True
    else:
        print('invalid byr')
        return False

#iyr (Issue Year) - four digits; at least 2010 and at most 2020.
def iyr_valid(v):
    year = int(v)
    if year >= 2010 and year <= 2020:
        return True
    else:
        print('invalid iyr')
        return False

#eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
def eyr_valid(v):
    year = int(v)
    if year >= 2020 and year <= 2030:
        return True
    else:
        print('invalid eyr')
        return False

#hgt (Height) - a number followed by either cm or in:
#    If cm, the number must be at least 150 and at most 193.
#    If in, the number must be at least 59 and at most 76.
def hgt_valid(v):
    #print(v)
    if v.endswith('cm') == False and v.endswith('in') == False:
        print('invalid hgt',v)
        return False
    h = int(v[0:len(v)-2])
    #print(h)
    if v.endswith('cm'):
        if h >= 150 and h <= 193:
            return True
        else:
            print('invalid hgt', v)
            return False

    if v.endswith('in'):
        if h >= 59 and h <= 76:
            return True
        else:
            print('invalid hgt', v)
            return False

    print('invalid hgt')
    return False

#hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
def hcl_valid(v):
    if len(v) == 7:
        if (v[0] != '#'):
            print('invalid hcl',v[0])
            return False
        for c in v[1:]:
            if c not in ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']:
                print('invalid hcl', c)
                return False
        return True
    else:
        print('invalid hcl ', len(v))
        return False

    print('invalid hcl')
    return False

#ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
def ecl_valid(v):
    if v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return True
    else:
        print("invalid ecl")
        return False

#pid (Passport ID) - a nine-digit number, including leading zeroes.
def pid_valid(v):
    if len(v) == 9:
        for c in v:
            d = int(c)
            if d < 0 and d > 9:
                print('invalid pid char',c)
                return False
        return True
            
    else:
        print('invalid pid')
        return False

    print('invalid pid')
    return False

#cid (Country ID) - ignored, missing or not.

def parse_passport(p):
    valid = ['byr','iyr','eyr','hgt','hcl','ecl','pid']

    found = []
    for item in p:
        k = item.split(':')[0]
        if (k in valid):
            valid.remove(k)
        
        found.append(k)
        v = item.split(':')[1]

        if k == 'byr':
            if byr_valid(v) == False:
                return 0
        if k == 'iyr':
            if iyr_valid(v) == False:
                return 0
        if k == 'eyr':
            if eyr_valid(v) == False:
                return 0
        if k == 'hgt':
            if hgt_valid(v) == False:
                return 0
        if k == 'hcl':
            if hcl_valid(v) == False:
                return 0
        if k == 'ecl':
            if ecl_valid(v) == False:
                return 0
        if k == 'pid':
            if pid_valid(v) == False:
                return 0
    
    if (len(valid) > 0):
        print("didn't find ",valid)
        return(0)
    else:
        print("good passport")
        return(1)

passport = []
num_valid = 0
for l in lines:
    temp = l.split(' ')
    for t in temp:
        if len(t) > 1:
            passport.append(t.strip())
    
    if len(l) == 1:
        print(passport)
        valid = parse_passport(passport)
        #print(valid)
        num_valid = num_valid + valid
        print("---")
        passport = []

#get the last one
print(passport)
valid = parse_passport(passport)
num_valid = num_valid + valid


print('number of valid passports ',num_valid)