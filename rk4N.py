import numpy as np
import pygame
import matplotlib.pyplot as plt


def rk4N(a, b, h, nfX0, dnfX, plotSpeed):
    if plotSpeed <= 0:
        return rk4NWithoutPlot(a, b, h, nfX0, dnfX)
    return rk4NWithPlot(a, b, h, nfX0, dnfX, plotSpeed)


def rk4NWithoutPlot(a, b, h, nfX0, dnfX):
    x = np.arange(a, b + h, h)
    n = len(x)
    order = len(nfX0)
    fnX = np.empty([order, n])
    fnX[:, 0] = nfX0.T
    k1, k2, k3, k4 = np.empty((1, order)), np.empty((1, order)), np.empty((1, order)), np.empty((1, order))
    for it in range(1, n):
        # k1
        for itOrder in range(order - 1):
            k1[0, itOrder] = fnX[itOrder + 1, it - 1]

        args = [x[it - 1]]

        for i in range(len(fnX)):
            args.append(fnX[i, it - 1])

        k1[0, order - 1] = dnfX(*args)

        # k2
        for itOrder in range(order - 1):
            k2[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k1[0, itOrder + 1]

        args = [x[it - 1] + h / 2]

        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k1[j][0])

        k2[0, order - 1] = dnfX(*args)

        # k3
        for itOrder in range(order - 1):
            k3[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k2[0, itOrder + 1]

        args = [x[it - 1] + h / 2]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k2[j][0])
        k3[0, order - 1] = dnfX(*args)

        # k4
        for itOrder in range(order - 1):
            k4[0, itOrder] = fnX[itOrder + 1, it - 1] + h * k3[0, itOrder + 1]

        args = [x[it - 1] + h]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h * k3[j][0])

        k4[0, order - 1] = dnfX(*args)

        for itOrder in range(order):
            fnX[itOrder, it] = fnX[itOrder, it - 1] + h / 6 * (
                    k1[0, itOrder] + 2 * k2[0, itOrder] + 2 * k3[0, itOrder] + k4[0, itOrder])

    fX = fnX[0, :]
    return fX, fnX


def rk4NWithPlot(a, b, h, nfX0, dnfX, plotSpeed):
    x = np.arange(a, b + h, h)
    n = len(x)
    order = len(nfX0)
    fnX = np.empty([order, n])
    fnX[:, 0] = nfX0.T
    k1, k2, k3, k4 = np.empty((1, order)), np.empty((1, order)), np.empty((1, order)), np.empty((1, order))
    for it in range(1, n):
        # k1
        for itOrder in range(order - 1):
            k1[0, itOrder] = fnX[itOrder + 1, it - 1]

        args = [x[it - 1]]

        for i in range(len(fnX)):
            args.append(fnX[i, it - 1])

        k1[0, order - 1] = dnfX(*args)

        # k2
        for itOrder in range(order - 1):
            k2[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k1[0, itOrder + 1]

        args = [x[it - 1] + h / 2]

        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k1[j][0])

        k2[0, order - 1] = dnfX(*args)

        # k3
        for itOrder in range(order - 1):
            k3[0, itOrder] = fnX[itOrder + 1, it - 1] + h / 2 * k2[0, itOrder + 1]

        args = [x[it - 1] + h / 2]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h / 2 * k2[j][0])
        k3[0, order - 1] = dnfX(*args)

        # k4
        for itOrder in range(order - 1):
            k4[0, itOrder] = fnX[itOrder + 1, it - 1] + h * k3[0, itOrder + 1]

        args = [x[it - 1] + h]
        for i in range(len(fnX)):
            for j in range(len(k1)):
                args.append(fnX[i, it - 1] + h * k3[j][0])

        k4[0, order - 1] = dnfX(*args)

        for itOrder in range(order):
            fnX[itOrder, it] = fnX[itOrder, it - 1] + h / 6 * (
                    k1[0, itOrder] + 2 * k2[0, itOrder] + 2 * k3[0, itOrder] + k4[0, itOrder])
        plt.plot(x, fnX[0, :], 'blue', [a, b], [0, 0], 'black')
        plt.pause(1 / plotSpeed)

s0T = 0
v0T = 10

# s"(t) = a
# s(0) = 0, s'(0) = 0
# rešenje: s(t) = v0.*t + F/m*0.5*t.^2

ddsT = lambda x, s, ds: 0
# ddsT = lambda *args: F/m
ns0T = np.array([s0T, v0T])

ta = 0
tb = 10
h = (tb - ta) / 10000

t = np.arange(ta, tb + h, h)

f_true = np.dot(v0T, t)
f_x_rk4, sss1 = rk4N(ta, tb, h, ns0T, ddsT, 0.0)

s10 = f_x_rk4[-1]
print(s10)


