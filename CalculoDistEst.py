import numpy as np
from discreteMarkovChain import markovChain
import discreteMarkovChain
P = np.array([[0.99,0.01,0.00,0.00,0.00,0.00],[0.00,0.80,4/100,1/100,0.00,0.15],[0.00,0.15,0.80,0.05,0.00,0.00],[0.00,0.00,0.05,0.80,0.15,0.00],[0.00,0.00,0.00,0.00,1.00,0.00],[0,0,0,0,0,1]])
mc = markovChain(P,['S','I','H','UCI','O','R'])
mc.computePi('krylov') #We can also use 'power', 'krylov' or 'eigen'
print(np.round(mc.pi,3))
