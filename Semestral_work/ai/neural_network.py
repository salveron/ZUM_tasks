import random
import numpy as np

from utils import *


class NeuralNetwork:
    def __init__(self, weights=None, biases=None):
        if weights is None:
            self.weights = [np.random.rand(NN_INPUT_LAYER_SIZE, NN_HIDDEN_LAYER_1_SIZE),
                            np.random.rand(NN_HIDDEN_LAYER_1_SIZE, NN_HIDDEN_LAYER_2_SIZE),
                            np.random.rand(NN_HIDDEN_LAYER_2_SIZE, NN_OUTPUT_LAYER_SIZE)]
        else:
            self.weights = weights

        if biases is None:
            self.biases = [np.ones((1, NN_HIDDEN_LAYER_1_SIZE)),
                           np.ones((1, NN_HIDDEN_LAYER_2_SIZE)),
                           np.ones((1, NN_OUTPUT_LAYER_SIZE))]
        else:
            self.biases = biases

    def forward_propagation(self, input_array):
        result = input_array.copy()
        for weights, biases in zip(self.weights, self.biases):
            result = sigmoid(np.dot(result, weights) + biases)
        return result

    def mutate(self, rate):
        return NeuralNetwork(weights=list(map(np.vectorize(lambda x: element_mutation(x, rate)), self.weights)),
                             biases=list(map(np.vectorize(lambda x: element_mutation(x, rate)), self.biases)))

    def cross(self, other, rate):  # One-point crossover
        if random.uniform(0.0, 1.0) > rate:  # Crossover will not occur
            return NeuralNetwork(weights=self.weights.copy(), biases=self.biases.copy()), \
                   NeuralNetwork(weights=other.weights.copy(), biases=other.biases.copy())

        # Computing offsprings' weights and biases
        offw_1, offw_2, offb_1, offb_2 = [], [], [], []
        for pw_1, pw_2, pb_1, pb_2 in zip(self.weights, other.weights, self.biases, other.biases):
            assert pw_1.shape == pw_2.shape and pb_1.shape == pb_2.shape

            # Crossing the weights (matrices) in the random point
            rand_row, rand_col = random.randrange(0, pw_1.shape[0]), random.randrange(0, pw_1.shape[1])
            offw_1.append(np.vstack((pw_1[:rand_row],
                                     np.hstack((pw_1[rand_row][:rand_col], pw_2[rand_row][rand_col:])),
                                     pw_2[rand_row + 1:])))
            offw_2.append(np.vstack((pw_2[:rand_row],
                                     np.hstack((pw_2[rand_row][:rand_col], pw_1[rand_row][rand_col:])),
                                     pw_1[rand_row + 1:])))

            # Crossing the biases (vectors) in the random point
            rand_idx = random.randint(0, pb_1.shape[0])
            offb_1.append(np.concatenate((pb_1[:rand_idx], pb_2[rand_idx:]), axis=0))
            offb_2.append(np.concatenate((pb_2[:rand_idx], pb_1[rand_idx:]), axis=0))

        return NeuralNetwork(weights=offw_1, biases=offb_1),\
               NeuralNetwork(weights=offw_2, biases=offb_2)


def sigmoid(input_array):
    return 1 / (1 + np.exp(-input_array))


def element_mutation(a, rate):
    if random.uniform(0.0, 1.0) <= rate:
        return a + random.uniform(-1.0, 1.0)
    else:
        return a
