import math
def solution(area):
    res = []
    total = area
    intitT = area
    rem = 0
    while(total != 1):
        root = math.sqrt(total)
        if (int(root + 0.5) ** 2 == total):
            print(total)
            res.append(total)
            total -= total
            
            
        else:
            print("out")
            area -= 1
    res.sort(reverse=True)
    return res


v = solution(15324)
print(v)
