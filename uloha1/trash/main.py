
import sympy as simp
import random
from matplotlib import pyplot as plt
# This is a sample Python script.
## ŕovnice je f(x,y) = c*(x+y** +x*y)  omega = x,y>=0 ; x+2y<4
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def disteribFce(x):

    return 1/512*x*(x*x*x -16*x*x + 48*x+128)


def postup2():
    x = simp.Symbol("x")
    y = simp.Symbol("y")
    fun = (1-x-y)
    eq1 = simp.integrate(fun, (x, 0, 4 - 2 * y))
    eq2 = simp.integrate(eq1, (y, 0, 2))
    c = 1 / eq2
    eq1 = c*(fun)
    max =  eq1.subs([(x,0),(y,0)])
    pts_y = []
    pts_x = []
    size = 200
    accuracy = 1e6
    for i in range(size):
        xx = random.randint(0, accuracy) / float(accuracy)
        yy = random.randint(0, accuracy) / float(accuracy)
        z = (random.randint(0, accuracy) / float(accuracy)) *max
        if xx+yy <1:
            if z <= eq1.subs([(x,xx),(y,yy)]):
                print()
                print("z", z, eq1, "=", eq1.subs([(x, xx), (y, yy)]))
                pts_x.append(xx)
                pts_y.append(yy)
    plt.scatter(pts_x, pts_y, c="blue")
    plt.show()


def print_hi(name):
    x = simp.Symbol("x")
    y = simp.Symbol("y")
    fun = (x + y ** 2 + x * y)
    eq1 = simp.integrate(fun, (x, 0, 4 - 2 * y))
    eq2 = simp.integrate(eq1, (y, 0, 2))
    c = 1 / eq2
    eq1 = simp.integrate(c * fun, (y, 0, (4 - x) / 2))
    Feq2 = simp.integrate(eq1, (x, 0, x))

    Feq2_1 =  Feq2

    pts_x = []
    pts_y = []
    for i in range(100):
        ran = random.randint(1, 10000) / 10000.0
        subs = simp.solve(Feq2_1-ran,(x),rational=True)
        for res in subs:
            if res >=0 and res<4:
                pts_x.append(res)
                pts_y.append(ran)

    plt.scatter(pts_x, pts_y, c="blue")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    postup2()
    #print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
