import matplotlib.pyplot as plt
import numpy as np


def plot_vectors(plot, som, vectors, vector_colors, key_words, N, title="", save=False):
    output = []
    plot.set_title(title)
    plot.title.set_size(30)
    for _, (t, c, vec) in enumerate(zip(key_words, vector_colors, vectors)):
        winnin_position = som.winner(vec)
        output.append(winnin_position)
        plot.text(winnin_position[0], winnin_position[1] + np.random.rand() * 0.5, t, fontsize=20, color=c)

    plot.set_xticks(range(N))
    plot.set_yticks(range(N))
    plot.grid()
    plot.set_xlim([0, N])
    plot.set_ylim([0, N])
    plot.plot()

    return output


def plot(som, vectors, vector_colors, key_words, title="", save=False):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111)
    output = plot_vectors(ax, som, vectors, vector_colors, key_words, som.get_weights().shape[0], title, save)
    if save:
        plt.savefig(f"{save}.png")
    return output
