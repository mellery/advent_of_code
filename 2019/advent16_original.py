from math import ceil
import time

def current_milli_time():
    return round(time.time() * 1000)

def get_multiplier(position, offset):
    base_pattern = [0,1,0,-1]
    if offset < position:
        return base_pattern[0]
    offset -= position
    return base_pattern[(offset // (position+1) + 1) % len(base_pattern)]

def get_digit(number, n):
    return number // 10**n % 10

def fft_phase(input, pattern):
    
    offset = [str(int) for int in input[0:8]]
    offset = int("".join(i for i in offset if i.isdigit()))
    print("offset",offset)
    #offset = input[0:8]

    #pattern = pattern * int(ceil(len(input)/len(pattern))+1)

    result = []

    for i in range(0,len(input)):

        digit = 0
        #if (-1 in temp_pattern):
            #print(i,len(input),temp_pattern)
        for x in range(i,len(input)):
            digit += input[x]*get_multiplier(i,x)
        #else:
        #    digit = sum(input[i:i+i+1])
            
        result.append(abs(digit)%10)

    return result

def flawed_frequency_transmission2(input, phases):
    i = (input[int(input[0:7]):])
    for a in range(phases):
        print(a)
        string = '' 
        e = 0
        while e < len(i):
            if e == 0:
                total = 0
                for f in i:
                    total += int(f)
            elif e > 0:
                total -= int(i[e-1])
            string += str(total)[-1]
            e+=1
        i = string
    print(i[0:8])

def flawed_frequency_transmission(input, phases):
    numbers = list(input)
    for i in range(0, len(numbers)):
        numbers[i] = int(numbers[i])

    pattern = [0,1,0,-1]
    last_time = 0
    for x in range(0,phases):
        print('PHASE',x, current_milli_time()-last_time)
        last_time = current_milli_time()
        numbers = fft_phase(numbers,pattern)
        #print(numbers)
    return numbers

#print(flawed_frequency_transmission('12345678',4)[0:8])

#print(flawed_frequency_transmission('80871224585914546619083218645595',100)[0:8])
#print(flawed_frequency_transmission('19617804207202209144916044189917',100)[0:8])
#print(flawed_frequency_transmission('69317163492948606335995924319873',100)[0:8])

#print(flawed_frequency_transmission('59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397',100)[0:8])

repeat = 10000

input = '03036732577212944063491565474664'
flawed_frequency_transmission2(input*repeat,100)

input = '02935109699940807407585447034323'
flawed_frequency_transmission2(input*repeat,100)

input = '03081770884921959731165446850517'
flawed_frequency_transmission2(input*repeat,100)

input = '59796737047664322543488505082147966997246465580805791578417462788780740484409625674676660947541571448910007002821454068945653911486140823168233915285229075374000888029977800341663586046622003620770361738270014246730936046471831804308263177331723460787712423587453725840042234550299991238029307205348958992794024402253747340630378944672300874691478631846617861255015770298699407254311889484508545861264449878984624330324228278057377313029802505376260196904213746281830214352337622013473019245081834854781277565706545720492282616488950731291974328672252657631353765496979142830459889682475397686651923318015627694176893643969864689257620026916615305397'
flawed_frequency_transmission2(input*repeat,100)
