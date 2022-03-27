import numpy as np
from scipy.special import expit as activation_function
from scipy.stats import truncnorm


def truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)


class NueralNetwork:
    def __init__(self,
                 no_of_in_nodes,
                 no_of_out_nodes,
                 no_of_hidden_A_nodes,
                 no_of_hidden_B_nodes):
        """NueralNetwork constructor

        Args:
            no_of_in_nodes (int): number of input nodes
            no_of_out_nodes (int): number of output nodes
            no_of_hidden_A_nodes (int): number of nodes in first hidden layer
            no_of_hidden_B_nodes (int): number of nodes in second hidden layer
        """
        self.no_of_in_nodes = no_of_in_nodes
        self.no_of_out_nodes = no_of_out_nodes
        self.no_of_hidden_A_nodes = no_of_hidden_A_nodes
        self.no_of_hidden_B_nodes = no_of_hidden_B_nodes
        self.create_weight_matrices()

    def create_weight_matrices(self):
        """A method to initialize the weight matrices of the neural network
        """
        rad = 1 / np.sqrt(self.no_of_in_nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_in_hidden_A = X.rvs((
            self.no_of_hidden_A_nodes,
            self.no_of_in_nodes
        ))

        rad = 1 / np.sqrt(self.no_of_hidden_A_nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_hidden_A_hidden_B = X.rvs((
            self.no_of_hidden_B_nodes,
            self.no_of_hidden_A_nodes
        ))

        rad = 1 / np.sqrt(self.no_of_hidden_B_nodes)
        X = truncated_normal(mean=0, sd=1, low=-rad, upp=rad)
        self.weights_hidden_B_out = X.rvs((
            self.no_of_out_nodes,
            self.no_of_hidden_B_nodes
        ))

    def run(self, input_vector):
        """running the network with an input vector 'input_vector'.

        Args:
            input_vector (tuple or list or ndarray): input vector

        Returns:
            ndarray: output vector
        """
        # Turn the input vector into a column vector:
        input_vector = np.array(input_vector, ndmin=2).T
        # activation_function() implements the expit function,
        # which is an implementation of the sigmoid function:
        hidden_A = activation_function(
            self.weights_in_hidden_A @ input_vector
        )
        hidden_B = activation_function(
            self.weights_hidden_A_hidden_B @ hidden_A
        )
        output_vector = activation_function(
            self.weights_hidden_B_out @ hidden_B
        )
        return output_vector
