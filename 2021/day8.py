from os import remove


def get_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return lines

def part1(filename):
        lines = get_lines(filename)
        count = 0
        for l in lines:
            in_segs = l.split('|')[0].strip()
            out_segs = l.split('|')[1].strip()
            temp = (in_segs + ' ' + out_segs).split(' ')
            
            segments = []
            for t in temp:
                #print(t,"".join(sorted(t)))
                segments.append("".join(sorted(t)))
                        
            ans = dict()
            for s in segments:
                if len(s) in [2,4,3,7]:
                    if len(s) == 2:
                        ans[1] = s
                    if len(s) == 4:
                        ans[4] = s
                    if len(s) == 3:
                        ans[7] = s
                    if len(s) == 7:
                        ans[8] = s

                    #print(s,len(s))
                    #count = count+1
            
# 1111
#2    3
#2    3
# 4444
#5    6
#5    6
# 7777 
            
            

            option = []
            for i in range(0,10):
                option.append(set(segments))

            for k,v in ans.items():
                option[k] = [v]
                for i in range(0,10):
                    if i != k:
                        if v in option[i]:
                            option[i].remove(v)

            if len(option[1]) == 1:
                a = list(option[1][0])
                
                for i in [2,5,6]:
                    templist = option[i].copy()
                    for t in templist:
                        if all(item in t for item in a) == True:
                            #print(1,t,"cant be",i)
                            option[i].remove(t)
            
            if len(option[4]) == 1:
                a = list(option[4][0])
                for i in [0,2,3,5,6,7]:
                    templist = option[i].copy()
                    for t in templist:
                        if all(item in t for item in a) == True:
                            #print(4,t,"cant be",i)
                            option[i].remove(t)

                            
            if len(option[7]) == 1:
                a = list(option[7][0])
                for i in [2,4,5,6]:
                    templist = option[i].copy()
                    for t in templist:
                        if all(item in t for item in a) == True:
                            #print(7,t,"cant be",i)
                            option[i].remove(t)

            S1temp = list(option[7][0])
            
            for a in list(option[1][0]):
                S1temp.remove(a)
            S1 = S1temp[0]
            

            S2_4temp = list(option[4][0])
            for a in list(option[1][0]):
                S2_4temp.remove(a)
            S2_4 = S2_4temp
            


            for i in [0,2,3]:
                templist = option[i].copy()
                for t in templist:
                    if all(item in t for item in S2_4) == True:
                        option[i].remove(t)

            if len(option[2]) == 1:
                option[2] = list(option[2])
            
            for i in [0,1,3,4,5,6,7,8,9]:
                templist = option[i].copy()
                for a in templist:
                    if a == option[2][0]:
                        option[i].remove(a)

            for i in range(0,10):
                templist = option[i].copy()
                for a in templist:
                    if i in [0,6,9] and len(a) != 6:
                        option[i].remove(a)
                    if i in [3,5] and len(a) != 5:
                        option[i].remove(a)



            for i in range(0,10):
                if len(option[i]) == 1:
                    option[i] = list(option[i])

            S5temp = list(option[6][0])
            for a in list(option[5][0]):
                S5temp.remove(a)
            S5 = S5temp[0]


            templist = list(option[9])
            
            for t in templist:
                #print(t)    
                if S5 in t:
                    #print("remove",t)
                    option[9].remove(t)

            for i in range(0,10):
                if len(option[i]) == 1:
                    option[i] = "".join(list(option[i]))

            #for i in range(0,10):
                #print(i,option[i])
            
            out_segs = out_segs.split(" ")
            ans = []
            for o in out_segs:
                temp = "".join(sorted(o))
                for i in range(0,10):
                    if option[i] == temp:
                        ans.append(str(i))
            ans_str = "".join(ans)
            print(ans_str)
            count += int(ans_str)
                
            
        return count

def part2(filename):
        lines = get_lines(filename)

def main():
    #print(part1("day8_ex1.txt"))
    #print(part1("day8_ex1.txt"))
    print(part1("day8_input.txt"))

    #print(part2("day8_ex1.txt"))
    #print(part2("day8_input.txt"))

if __name__ == "__main__":
    main()