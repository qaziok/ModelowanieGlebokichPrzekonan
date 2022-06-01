import matplotlib.pyplot as plt
import numpy as np


def plot_vectors(som, vectors, vector_colors, key_words, N):
    x = plt.figure(figsize=(20, 20))

    for _, (t, c, vec) in enumerate(zip(key_words, vector_colors, vectors)):
        winnin_position = som.winner(vec)
        plt.text(winnin_position[0], winnin_position[1] + np.random.rand() * .9, t, fontsize=30, color=c)

    plt.xticks(range(N))
    plt.yticks(range(N))
    plt.grid()
    plt.xlim([0, N])
    plt.ylim([0, N])
    plt.plot()
    plt.show()
    plt.close(x)
