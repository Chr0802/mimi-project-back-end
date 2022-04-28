a = [3, 1, 1, 4, 5, 6]


def fanhui(a):
    fzs = []
    tem = []
    for j in range(1, len(a) + 1):
        if j == 1:
            fzs.append(j)
        if j > 1:
            for i in range(2, j):
                if (j % i) == 0:
                    fzs.append(j)
                    break
    for i in range(1, len(a) + 1):
        if i not in fzs:
            tem.append(a[i - 1])
    a = tem

    while len(a) != 1:
        a = fanhui(a)
    return a


print(fanhui(a))


