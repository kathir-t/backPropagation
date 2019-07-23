# 2 layered back propogation algorithm
import numpy as np
import timeit

x = [ [0.5, -0.5], [-0.5, 0.5]]
d = [ [0.9, 0.1], [0.1, 0.9]]
wjk = [ [0.1, 0.3], [-0.2, 0.55]]
wij = [ [0.37, -0.22], [0.9, -0.12]]

ipCount = len(x[0])
iterationsLimit = 2000
breakIfErrorLow = True
errorThreshold = 0.00001

def findH():
    h = []
    for n in range(ipCount):
        tempH = 0
        for m in range(ipCount):
            tempH = tempH + (wjk[m][n] * x[curPattern][m])
        h.append(tempH)
    return h

def findV(hArray):
    v = []
    for h in hArray:
        v.append(1 / (1 + np.exp(-1 * h)))
    return v

def findS(v):
    s = []
    for n in range(ipCount):
        tempS = 0
        for m in range(ipCount):
            tempS = tempS + (wij[m][n] * v[m])
        s.append(tempS)
    return s

def findY(sArray):
    y = []
    for s in sArray:
        y.append(1 / (1 + np.exp(-1 * s)))
    return y

def findError(y):
    return np.subtract(d[curPattern],y)

def delta(y):
    return y * (np.subtract(1,y)) * (np.subtract(d[curPattern],y))

def deltaH(v, delta):
    delHarray = []
    for n in range(ipCount):
        temp = 0
        for m in range(ipCount):
            temp = temp + (delta[m] * wij[n][m])
        tempDH = v[m] * (1 - v[m]) * (temp)
        delHarray.append(tempDH)
    return delHarray

start = timeit.default_timer()

for iteration in range(iterationsLimit):
    for pattern in range(len(x)):
        global curPattern
        curPattern = pattern
        h = findH()
        # print("h = " + str(h))
        v = findV(h)
        # print("v = " + str(v))
        s = findS(v)
        # print("s = " + str(s))
        y = findY(s)
        # print("y = " + str(y))
        e = findError(y)
        # print("e = " + str(e))
        de = delta(y)
        # print("de = " + str(de))
        dH = deltaH(v,de)
        # print("dH = " + str(dH))

        for n in range(ipCount):
            for m in range(ipCount):
                wij[m][n] = wij[m][n] + (de[n] * v[m])
                wjk[m][n] = wjk[m][n] + (dH[n] * x[curPattern][m])
    print("Iteration : " + str(iteration), end="\t")
    print(" Error :", end="\t")
    print(e)
    if breakIfErrorLow:
        if max(abs(e)) <= errorThreshold:
            print("Error criteria met. Exiting loop")
            break
        elif iteration == iterationsLimit-1:
            print("Error criteria was not met. Exiting loop due to max iterations limit")


stop = timeit.default_timer()
print("Wjk ", wjk)
print("Wij ", wij)
print('Runtime: ', stop - start, " seconds")
