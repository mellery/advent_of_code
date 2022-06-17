def get_point_pairs(filename):
    with open(filename) as f:
        lines = f.readlines()
        numbers = []
        grid = {}
        start_point = []
        end_point = []
        for l in lines:
            points = l.split(' ')
            p1 = points[0].strip()
            p1x = int(p1.split(',')[0])
            p1y = int(p1.split(',')[1])
            start_point.append((p1x,p1y))
            p2 = points[2].strip()
            p2x = int(p2.split(',')[0])
            p2y = int(p2.split(',')[1])
            end_point.append((p2x,p2y))
            #print(f"({p1x},{p1y})->({p2x},{p2y})")
    for i in range(0,len(start_point)):
        #print(start_point[i],end_point[i])

        if start_point[i][0] == end_point[i][0]: #horizontal
            #print("h",start_point[i],"->",end_point[i])
            if start_point[i][1] > end_point[i][1]:
                for x in range(end_point[i][1],start_point[i][1]+1):
                    point = (start_point[i][0],x)
                    #print(point)
                    if point in grid:
                        grid[point] += 1
                    else:
                        grid[point] = 1
            else:
                for x in range(start_point[i][1],end_point[i][1]+1):
                    point = (start_point[i][0],x)
                    
                    if point in grid:
                        grid[point] += 1
                    else:
                        grid[point] = 1


        elif start_point[i][1] == end_point[i][1]: #vertical
            #print("v",start_point[i],"->",end_point[i])
            if start_point[i][0] > end_point[i][0]:
                for x in range(end_point[i][0],start_point[i][0]+1):
                    point = (x,start_point[i][1])
                    #print(point)
                    if point in grid:
                        grid[point] += 1
                    else:
                        grid[point] = 1
            else:
                for x in range(start_point[i][0],end_point[i][0]+1):
                    point = (x,start_point[i][1])
                        
                    if point in grid:
                        grid[point] += 1
                    else:
                        grid[point] = 1
        else:
            slope = (end_point[i][1]-start_point[i][1])/(end_point[i][0]-start_point[i][0])
            #print(f"slope {slope}, {start_point[i]},{end_point[i]}")
            if start_point[i][0] > end_point[i][0]:
                if slope == 1:
                    #print(f"slope {slope}, {end_point[i]},{start_point[i]}")
                    temp = 0
                    for x in range(end_point[i][0],start_point[i][0]+1):
                        point = (x,end_point[i][1]+temp)
                        if point in grid:
                            grid[point] += 1
                        else:
                            grid[point] = 1
                        temp += 1
                elif slope == -1:
                    print(f"slope {slope}, {end_point[i]},{start_point[i]}")
                    temp = 0
                    for x in range(end_point[i][0],start_point[i][0]+1):
                        point = (x,end_point[i][1]+temp)
                        if point in grid:
                            grid[point] += 1
                        else:
                            grid[point] = 1
                        temp -= 1
                

            else:
                if slope == 1:
                    #print(f"slope {slope}, {end_point[i]},{start_point[i]}")
                    temp = 0
                    for x in range(start_point[i][0],end_point[i][0]+1):
                        point = (x,start_point[i][1]+temp)
                        if point in grid:
                            grid[point] += 1
                        else:
                            grid[point] = 1
                        temp += 1
                elif slope == -1:
                    print(f"slope {slope}, {start_point[i]},{end_point[i]}")
                    temp = 0
                    for x in range(start_point[i][0],end_point[i][0]+1):
                        point = (x,start_point[i][1]+temp)
                        if point in grid:
                            grid[point] += 1
                        else:
                            grid[point] = 1
                        temp -= 1
            
    return grid

def part1(filename):
    grid = get_point_pairs(filename)
    count = 0 
    for k,i in grid.items():
        if i > 1:
            print(k,i)
            count += 1
    print(count)
        

def part2(filename):
    grid = get_point_pairs(filename)
    count = 0 
    for k,i in grid.items():
        if i > 1:
            #print(k,i)
            count += 1
    print(count)
        

def main():
    day = '5'
    #print(part1(f"day{day}_ex1.txt"))
    #print(part1(f"day{day}_input.txt"))

    #print(part2(f"day{day}_ex1.txt"))
    print(part2(f"day{day}_input.txt"))

if __name__ == "__main__":
    main()