def print_cups(cups,current):
    ans = "cups: "
    for c in cups:
        if current == c:
            ans = ans + '('+str(c)+') '
        else:
            ans = ans + str(c) + ' '
    print(ans)

def print_cups_dict(dcups,current):
    ans = "dcups: "
    for x in range(0,len(dcups)):
        ans = ans + str(dcups[current]) + ' '
        current = dcups[current]

    print(ans)

def cupgame(input,moves, part):
    #print(input,"moves",moves, "part",part)
    dcurrent = int(input[0])
    
    index = int(max(input))
    while len(input) < 1000000:
        index = index + 1
        input.append(index)
    #print(input)

    dcups = {}
    for x in range(0,len(input)-1):
        dcups[int(input[x])] = int(input[x+1])
    dcups[int(input[len(input)-1])] = int(input[0])

    #print(dcups)
    maxdcup = max(dcups)

    for m in range(0,moves):
        
        if m > 0:
            dcurrent = dcups[dcurrent]
        
        if m%100000==0:
            print("-- move:",m+1,"--")
        #print_cups_dict(dcups,dcurrent)
        
        dpickup = []
        dp = dcups[dcurrent]
        for x in range(0,3):
            dpickup.append(dp)
            dp = dcups[dp]

        #print("dpickup:",dpickup)

        ddestination = dcurrent - 1
        
        if ddestination == 0:
            ddestination = maxdcup #max(dcups)

        while ddestination in dpickup:
            ddestination = ddestination - 1
            if ddestination == 0: #min(dcups):
                ddestination = maxdcup #max(dcups)
        
        #print("ddestination:",ddestination)
        #print("dcurrent",dcurrent)

        templink = dcups[ddestination]
        
        dcups[ddestination] = dcups[dcurrent]
        dcups[dcurrent] = dcups[dpickup[2]]
        dcups[dpickup[2]] = templink

    dcurrent = dcups[dcurrent]

    #print('\n-- final --') 
    #print_cups_dict(dcups,dcurrent)

    print(dcups[1])
    print(dcups[dcups[1]])
    print(dcups[1] * dcups[dcups[1]])
    #1. crab picks up 3 times clockwise of the current cup
    #2. crab selects destination cup with label equal to current cup -1, or -1 till cup found, or wraps around
    #3. crab inserts the cups clockwise of destination cup
    #4. get new current cup


#cupgame(list('389125467'), 10, 1)
#cupgame(list('389125467'), 100, 1)
#cupgame(list('784235916'), 100, 1)

#cupgame(list('389125467'), 10000000, 2)
cupgame(list('784235916'), 10000000, 2)
#cupgame(list('54321'),20,2)