import math

import matplotlib.pyplot as plt


def eulerus_plus(func, x0, y0, a, b, h):
    y = [y0]
    x = []
    n = int((b - a) / h)

    for i in range(n + 1):
        x += [x0 + i * h]
    for i in range(n):
        yi = y[i]
        value = yi + h / 2 * (func(x[i], yi) + func(x[i + 1], yi + h * func(x[i], yi)))
        y += [value]

    return x, y


def adams(func, x0, a, b, h, y1):
    x = []
    y = y1
    n = int((b - a) / h)
    for i in range(n + 1):
        x += [x0 + i * h]

    for i in range(3, n):
        df = []
        df += [func(x[i], y[i]) - func(x[i - 1], y[i - 1])]
        df += [func(x[i], y[i]) - 2 * func(x[i - 1], y[i - 1]) + func(x[i - 2], y[i - 2])]
        df += [
            func(x[i], y[i]) - 3 * func(x[i - 1], y[i - 1]) + 3 * func(x[i - 2], y[i - 2]) - func(x[i - 3], y[i - 3])]
        value = y[i] + h * func(x[i], y[i]) + pow(h, 2) / 2 * df[0] + 5 / 12 * pow(h, 3) * df[1] + 3 / 8 * pow(h, 4) * \
                df[2]
        y += [value]

    return x, y


def draw_graph(x, y, equation, name):
    eq_name = {1: "y' = y + (1+x)y\u00b2",
               2: "y' = y/x - 3",
               3: "y' = x\u00b2 - 2y"}
    ax = plt.gca()
    plt.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.title(name + ": график уравнения " + eq_name[equation])
    plt.plot(x, y, color='r', linewidth=2)
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color='r', s=20)
    plt.show()


def draw_all(x, y_eulerus, y1, equation):
    # eq_name = {1: "y' = y + (1+x)y\u00b2",
    #            2: "y' = y/x - 3",
    #            3: "y' = x\u00b2 - 2y"}

    if equation == 1:
        example_func = lambda x: (-math.exp(x)) / (x * math.exp(x) + ((-math.exp(x0) / y0) - x0 * math.exp(x0)))
        y_example = [example_func(x) for x in x]
        plt.plot(x, y_example, color='b', linewidth=1, label = "accurate")
    ax = plt.gca()
    plt.grid()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.plot(x, y_eulerus, color='r', linewidth=2, label = "Eulerus")
    for i in range(len(x)):
        plt.scatter(x[i], y_eulerus[i], color='r', s=20)

    plt.plot(x, y1, color='g', linewidth=2, label = "Adams")

    for i in range(len(x)):
        plt.scatter(x[i], y1[i], color='g', s=20)

    ax.legend()
    plt.show()


if __name__ == '__main__':
    print("Выберите уравнение:")
    print("\t1. y' = y + (1+x)y\u00b2\n"
          "\t2. y' = y/x - 3\n"
          "\t3. y' = x\u00b2 - 2y")
    e = int(input())
    func = None
    if e == 1:
        func = lambda x, y: y + (1 + x) * pow(y, 2)
    elif e == 2:
        func = lambda x, y: y / x - 3
    elif e == 3:
        func = lambda x, y: pow(y, 2) - 2 * y
    x0 = float(input("x0: "))
    y0 = float(input("y0: "))
    a, b = map(float, input("Интервал [a, b]: ").split())
    h = float(input("h: "))
    eps = float(input("\u03b5: "))

    print("Улучшенный метод Эйлера")
    while True:
        x1, y1 = eulerus_plus(func, x0, y0, a, b, h)
        x2, y2 = eulerus_plus(func, x0, y0, a, b, 2 * h)
        if len(y1) >= 3:
            print("\nШаг " + str(h))
            print(abs(y1[-1] - y2[-1]))
            for i in range(len(x1)):
                print("{:< 10.6} {:< 10.6} ".format(x1[i], y1[i]))
            print()
            if (abs(y1[-1] - y2[-1]) / 3) > eps:
                h /= 2
            else:
                print("Точность достигнута при h = " + str(h))
                break
        else:
            print("Количество разбиений мало, шаг уменьшен")
            h /= 2
    y_eulerus = y1
    draw_graph(x1, y1, e, "усов. метод Эйлера")

    print("\nМетод Адамса:")
    while True:
        x1, y1 = adams(func, x0, a, b, h, y1[0:4])
        # x2, y2 = adams(func, x0, a, b, 2 * h, y1[0:4])
        print("\nШаг " + str(h))
        for i in range(len(x1)):
            print("{:< 10.6} {:< 10.6}".format(x1[i], y1[i]))
        print()
        # print(y1[2], y2[1])
        # if (abs(y1[2] - y2[1]) / 15) > eps:
        #     h /= 2
        # else:
        #     print("Точность достигнута при h = " + str(h))
        break

    draw_graph(x1, y1, e, "метод Адамса")
    draw_all(x1, y_eulerus, y1, e)
