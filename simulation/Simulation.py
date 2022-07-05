from minisom import MiniSom
from simulation.simulation_setup import *
from preprocessing.vectors import tfidf_vectors
from copy import deepcopy
from som.plot import plot
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import pandas as pd


class Simulation:
    def __init__(self, title, knowledge, key_words, close_words):
        """
        Symulacja czytania artukułów przez osobę z określonymi z góry poglądami

        :param title: Opis osoby
        :param knowledge: Wiedza osoby
        :param key_words: Słowa kluczowe
        :param close_words: Słowa sąsiadujące ze słowami kluczowymi
        """
        self.title = title
        self.knowledge = knowledge
        self.key_words = key_words
        self.close_words = close_words
        self.training_statistics = {}
        self.reading = ''

        # generate vectors to train SOM
        vectors = tfidf_vectors(knowledge, key_words, close_words)
        self.som = MiniSom(size, size, len(vectors[0]), sigma=sigma, learning_rate=learning_rate,
                           activation_distance=activation_distance)

        print('training...')
        self.som.train(vectors, knowledge_iterations, verbose=True)

        self.__plot(self.som, vectors, title, 'knowledge')

    def run(self, to_read, what_to_read=None):
        """
        Uruchamia symulację

        :param to_read: Artykuły do przeczytania
        :param what_to_read: Opis artyków do przeczytania
        :return: tablica z sumami i średniami dla pro i anty przy kolejnych wartościach learning rate
        """
        self.reading = f'_{what_to_read}'
        vectors = tfidf_vectors(to_read, self.key_words, self.close_words)
        for lr in [0.01, 0.05, 0.1, 0.15, 0.25, 0.5, 1]:
            print(f'learning rate = {lr}')
            self.__read(vectors, lr)
        table = pd.DataFrame(self.training_statistics)
        table.to_csv(f'simulations_storage/tables/{self.title}{self.reading}_table.csv')
        self.reading = ''
        return table

    def __read(self, vectors: list, lr: float):
        title = f'{self.title}_reads{self.reading} dla learning rate = {lr}'
        new = MiniSom(*self.som.get_weights().shape, sigma=2 * sigma, learning_rate=lr,
                      activation_distance=activation_distance)
        new._weights = deepcopy(self.som.get_weights())
        new.train(vectors, reading_iterations, verbose=True)

        self.__plot(new, vectors, title, lr)

    def __plot(self, som, vectors, title, lr):
        print('plotting...')
        middle = keywords_length // 2
        vectors_colors = ['g'] * middle + ['r'] * middle

        points = plot(som, vectors, vectors_colors, self.key_words, title,
                      f'simulations_storage/plots/{self.title}{self.reading}_{lr}')

        points_pro = points[:middle]
        points_anti = points[middle:]
        sum_pro, mean_pro = self.__distance_sum_mean(points_pro)
        sum_anti, mean_anti = self.__distance_sum_mean(points_anti)
        self.training_statistics[lr] = {'sum_pro': sum_pro, 'mean_pro': mean_pro,
                                        'sum_anti': sum_anti, 'mean_anti': mean_anti}

    @staticmethod
    def __distance_sum_mean(points):
        distances = euclidean_distances(points, points)
        return np.sum(distances), np.mean(distances[distances != 0])


if __name__ == "__main__":
    pass
