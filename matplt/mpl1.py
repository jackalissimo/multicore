import numpy as np
from matplotlib import (
    pyplot as plt
)

def parab(x, a, b, c):
    return a * x ** 2 + b * x + c


def draw_parab():
    # xlist = np.linspace(-10, 10, num=1000)
    xlist = np.arange(-10, 10, 0.1)
    a = 3
    b = 1
    c = 33
    ylist = parab(xlist, a, b, c)
    plt.figure(num=0, dpi=120)
    plt.plot(xlist, ylist, label="f(x)")
    plt.plot(xlist, ylist ** 0.75, linestyle='--', color='#6A2', label=r"f(x)$^{0.75}$")
    plt.title("Have a good day!")
    plt.xlabel("distance / m")
    plt.ylabel("height / m")
    plt.legend()
    plt.show()

    # inp = str(input())
    # print("you typed \"{}\".".format(inp))


def main():
    draw_parab()

if __name__ == "__main__":
    main()

