import matplotlib.pyplot as plt
import random

testlist = []


def rolldice(dice):
    return sorted([random.randint(1, 6) for i in range(dice)])


def convert(dlist):
    if dlist[0] == dlist[1] or dlist[1] == dlist[2]:
        # returning too many... need to fix
        return [6, 6]
    elif dlist[0] == dlist[1] and dlist[1] == dlist[2]:
        return [dlist[0], dlist[2]]
    elif dlist[1] - dlist[0] == 1:
        return [dlist[2], dlist[0]]
    elif dlist[2] - dlist[1] == 1:
        if sum(dlist) - 9 < 0:
            if sum(dlist) - 8 == 0:
                return [1, 1]
            else:
                return [1, sum(dlist) - 8]
        elif sum(dlist) - 8 == 0:
            # is this even possible?
            return [sum(dlist) - 9, 1]
        else:
            return [sum(dlist) - 9, sum(dlist) - 8]
    else:
        return [sum(dlist) - 7, sum(dlist) - 7]


def convert100():
    return list(map(lambda x: convert(rolldice(3)), range(100)))

test100 = convert100()

for i in range(100):
    for j in range(2):
        testlist.append(test100[i][j])

plt.hist(testlist)
plt.show()
