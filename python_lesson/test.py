weights = [2.5, 3.0, 4.5, 5.0]  # 重みの例
index = 0

def has_weight():
    global index
    return index < len(weights)

def get_weight():
    global index
    weight = weights[index]
    index += 1
    return weight

sum = 0
cnt = 0
while has_weight():
    w_tmp = get_weight()
    sum += w_tmp
    cnt += 1

if cnt > 0:
    w_target = sum / cnt
    print("Average weight:", w_target)
else:
    print("No weights available")
