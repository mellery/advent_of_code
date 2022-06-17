
def get_digit(number, n):
    return number // 10**n % 10

def repeated_digits(n):
    ans = []
    nstr = str(n)
    index = 0
    
    while index < len(nstr):
        if len(ans) == 0:
            index = 0
        else:
            index = sum(ans)

        if index < len(nstr):
            temp = nstr[index]
        else:
            print(n,ans)
            return ans

        count = 1
        if index+1 < len(nstr):
            for x in range(index+1,len(nstr)):
                if temp == nstr[x]:
                    count = count + 1
                else:
                    break
        ans.append(count)

    print(n,ans)
    return ans
    

low = 125730
high = 579381

ans = 0

for x in range(low,high+1):

    if get_digit(x,5) <= get_digit(x,4) <= get_digit(x,3) <= get_digit(x,2) <= get_digit(x,1) <= get_digit(x,0):
        if get_digit(x,5) == get_digit(x,4) or get_digit(x,4) == get_digit(x,3) or get_digit(x,3) == get_digit(x,2) or get_digit(x,2) == get_digit(x,1) or get_digit(x,1) == get_digit(x,0):
            if 2 in repeated_digits(x):
                print(x)
                ans = ans + 1

print(ans)
#1015 is too low