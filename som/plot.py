import matplotlib.pyplot as plt
import numpy as np


def plot_vectors(plot, som, vectors, vector_colors, key_words, N, title="", save=False):
    output = []
    plot.set_title(title)
    for _, (t, c, vec) in enumerate(zip(key_words, vector_colors, vectors)):
        winnin_position = som.winner(vec)
        output.append(winnin_position)
        plot.text(winnin_position[0], winnin_position[1] + np.random.rand() * .9, t, fontsize=20, color=c)

    plot.set_xticks(range(N))
    plot.set_yticks(range(N))
    plot.grid()
    plot.set_xlim([0, N])
    plot.set_ylim([0, N])
    plot.plot()

    return output
