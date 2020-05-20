import pytest

from ai.neural_network import NeuralNetwork
from utils import *


nn = NeuralNetwork()


def test_creation():
    assert len(nn.weights) == len(nn.biases) == NN_LAYERS - 1
    assert nn.weights[0].shape == (NN_INPUT_LAYER_SIZE, NN_HIDDEN_LAYER_1_SIZE)
    assert nn.weights[1].shape == (NN_HIDDEN_LAYER_1_SIZE, NN_HIDDEN_LAYER_2_SIZE)
    assert nn.weights[2].shape == (NN_HIDDEN_LAYER_2_SIZE, NN_OUTPUT_LAYER_SIZE)
    assert nn.biases[0].shape == (1, NN_HIDDEN_LAYER_1_SIZE)
    assert nn.biases[1].shape == (1, NN_HIDDEN_LAYER_2_SIZE)
    assert nn.biases[2].shape == (1, NN_OUTPUT_LAYER_SIZE)


def test_propagation():
    inputs = [1, ] * 12
    outputs = nn.forward_propagation(inputs)
    assert outputs.shape == (1, NN_OUTPUT_LAYER_SIZE)
    assert 0 <= outputs.all() <= 1
