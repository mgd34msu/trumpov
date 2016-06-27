# multi-line fibonacci sequence function
def fs1(x):
    if x == 0:
        return 0
    elif x == 1:
        return 1
    else:
        return fs1(x - 1) + fs1(x - 2)


for i in range(21):
    print(fs1(i))


# one-line fibonacci sequence function
def fs2(x):
    return x if x < 2 else fs2(x - 1) + fs2(x - 2)

for i in range(21):
    print(fs2(i))


# one-line fibonacci sequence lambda function
fs3 = lambda x: x if x < 2 else fs3(x - 1) + fs3(x - 2)

for i in range(21):
    print(fs3(i))


# one-liner fibonacci sequence (approximates golden ratio -- likely inaccurate at large fib values)
def fs4(x):
    return int(((1 + (5 ** 0.5)) / 2) ** x / (5 ** 0.5) + 0.5)


for i in range(21):
    print(fs4(i))

# -----------------------------------------------------------------------------------------------------


# one line function to check if a number is prime
def pc1(x):
    return False if x < 2 else all(x % i for i in range(2, x))

for i in range(101):
    print(i, pc1(i))
