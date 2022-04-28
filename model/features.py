from matplotlib import pyplot as plt


def f_importances(coef, names, *, limit=10):
    imp = coef[0]
    x = sorted(zip(imp, names))
    return x[:limit], x[-limit:]


def f_importances_graph(coef, names, *, limit=10):
    slowa_anty, slowa_pro = f_importances(coef, names,limit=limit)

    imp, names = zip(*(slowa_anty + slowa_pro))
    plt.barh(range(len(names)), imp, align='center')
    plt.yticks(range(len(names)), names)
    plt.show()

    return slowa_anty, slowa_pro


if __name__ == "__main__":
    f_importances_graph([[1, 2, 3]], [1, 2, 3], limit=2)
