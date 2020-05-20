# Genetic algorithm task

This is my implementation of the Genetic algorithm with crowding methods. It uses deterministic
or probabilistic replacement for getting better results of evolution.

## Running

 - `$ python3 main.py -s` will run a simple GA with default parameters (pop_size=20,
 num_of_gens=100, parents_percent=.4, cross_rate=.9, mutation_rate=.05)
 
 - `$ python3 main.py -s --handle 100 50 .7 .8 .1` will run a simple GA with given 
parameters (pop_size=100, num_of_gens=50, parents_percent=.7, cross_rate=.8, 
mutation_rate=.1)

 - `$ python3 main.py -cd` will run a GA that uses deterministic crowding with default
 parameters
 
 - `$ python3 main.py -cp --handle 100 50 .7 .8 .1` will run a GA that uses probabilistic
 crowding with given parameters, etc.
 
 **Warnings and experiments are described in the protocol for the task**
 
 
