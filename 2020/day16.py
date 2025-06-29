
filename = "day16_input.txt"
#filename = "day16_ex1.txt"
#filename = "day16_ex2.txt"

file1 = open(filename, 'r') 
lines = file1.readlines() 

fields = {}

your_ticket_found = False
nearby_tickets_found = False

myticket = []
tickets = []

for l in lines:
    temp = l.strip()
    
    #print(len(temp),temp)
    
    if len(temp) == 0:
        continue
    
    elif 'your ticket' in temp:
        your_ticket_found = True
    elif 'nearby tickets' in temp:
        nearby_tickets_found = True

    elif your_ticket_found == False and nearby_tickets_found == False:
        field = temp.split(':')[0]
        rulestr = temp.split(':')[1]
        rules = rulestr.split(' or ')
        fields[field] = rules

    elif your_ticket_found == True and nearby_tickets_found == False:
        myticket = temp.split(',')
    
    else:
        ticket = temp.split(',')
        tickets.append(ticket)

def validate_ticket(ticket):
    invalid = []
    for x in ticket:
        n = int(x)
        
        invalid_count = 0
        for field, rule in fields.items():
            low = int(rule[0].split('-')[0])
            hi = int(rule[0].split('-')[1])
            low2 = int(rule[1].split('-')[0])
            hi2 = int(rule[1].split('-')[1])
            
            if ((n >= low and n <= hi) or (n >= low2 and n <= hi2)) == False:
                invalid_count = invalid_count + 1
        if invalid_count == len(fields):
            invalid.append(n)
    return sum(invalid)
        
ans = 0
good_tickets = []
for t in tickets:
    result = validate_ticket(t)

    if result == 0:
        good_tickets.append(t)
    ans = ans + result    
print("answer",ans)

good_tickets.append(myticket)

options = {}
for field,rule in fields.items():
    temp = []
    for x in range(0,len(fields)):
        temp.append(x)
    options[field] = temp.copy()

#-----
for x in range(0,len(fields)):
    for field, rule in fields.items():
        
        if len(options[field]) > 1:

            option_count = 0
            tempopt = []
            for col in options[field]:
                valid_count = 0

                for t in good_tickets:
                    
                    n = int(t[col])
                    low = int(rule[0].split('-')[0])
                    hi = int(rule[0].split('-')[1])
                    low2 = int(rule[1].split('-')[0])
                    hi2 = int(rule[1].split('-')[1])
                    
                    if ((n >= low and n <= hi) or (n >= low2 and n <= hi2)) == True:
                        valid_count = valid_count + 1
            
                if valid_count == len(good_tickets):
                    option_count = option_count + 1
                    tempopt.append(col)

            if option_count == 1:
                options[field] = tempopt.copy()
                for o, v in options.items():
                    if tempopt[0] in v and o is not field:
                        v.remove(tempopt[0])
                break

depts = []
for o,v in options.items():
    print(o,v)
    if 'departure' in o:
        depts.append(int(v[0]))
print(depts)

ans = 1
for x in depts:
    ans = ans*int(myticket[x])
print(ans)
