week_temp = [[32,34,27,30,26,25,31],   \
             [28,24,29,31,34,31,32],   \
             [32,31,29,27,32,25,26],   \
             [29,28,35,32,26,31,33]
            ]

def week_average(a,w): #  w คือแถวสัปดาห์ที่ต้องการ w0 คือ สัปดาห์แรก
    sum = 0
    i = 0
    if w < 0 or w >= len(a):
        return "ไม่มีค่าอุณหภูมิเฉลี่ยในสัปดาห์ที่ต้องการ"
    while i < len(a[w]) :
        sum = sum + a[w][i]
        i = i + 1
    return sum / len(a[w])
print(week_average(week_temp,0))

def week_max(a,w):
    i = 1
    max = a[w][0]
    if w < 0 or w >= len(a):
        return "ไม่มีค่าอุณหภูมิเฉลี่ยในสัปดาห์ที่ต้องการ"
    while i < len(a[w]) :
        if max < a[w][i] :
           max = a[w][i] 
        i = i + 1
    return max
#print(week_max(week_temp,2))

def week_min(a,w):
    i = 1
    min = a[w][0]
    if w < 0 or w >= len(a):
        return "ไม่มีค่าอุณหภูมิเฉลี่ยในสัปดาห์ที่ต้องการ"
    while i < len(a[w]) :
        if a[w][i] < min :
           min = a[w][i] 
        i = i + 1
    return min
# print(week_min(week_temp,2))

def overall_max(a):
    best = week_max(a,0)
    i = 1
    while i < len(a) :
        max = week_max(a,i)
        if max > best :
            best = max 
        i = i + 1
    return best
print(overall_max(week_temp))

def overall_min(a):
    lowest = week_min(a,0)
    i = 1
    while i < len(a):
        min = week_min(a,i)
        if min < lowest : 
            lowest = min 
        return lowest
print(overall_min(week_temp)