# working with fucking long float numbers


def normalize(x):
    s = str(x - int(x))[::-1]
    print(s)
    if s[0] != '0' and s[1:5] == '0000':
        index = 1
        while s[index] == '0':
            index += 1
        s = s[index:][::-1]
        x = int(x) + float(s)
    elif s[0] != '9' and s[1:5] == '9999':
        index = 1
        while s[index] == '9':
            index += 1
        s = s[index:][::-1]
        x = int(x) + float(s) + 10 ** (-(len(s) - 2))
    print(x)
    return x


x = 0.00097648
y = 0.2 * 0.1
z = 0.01371356
w = (100 - 0.1) / 100 * 0.2
print(x)
print(y)
print(z)
print(w)
# print(normalize(x + y))
print(normalize(z - w))
