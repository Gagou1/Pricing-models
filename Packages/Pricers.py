import numpy as np
import math
import random


def MonteCarloPricer(model, options, steps, n):
    #options is an array that contains options objects stored in array whose first axis is time index
    rate=model.getRate()
    Times=np.zeros_like(options)
    for index in np.ndindex(options.shape):
        Times[index]=options[index].getTime()
    maxT=np.amax(Times)
    discount=np.zeros_like(options)
    for index in np.ndindex(options.shape):
        discount[index]=np.exp(-rate*Times[index])
    path=[model.createPath(steps,maxT) for _ in range(n)]
    prices=np.zeros_like(options)
    for index in np.ndindex(options.shape):
        prices[index]=np.mean(np.array([(discount[index])*options[index].payoff(path[i][0:math.floor(steps*Times[index]/maxT)+1]) for i in range(n)]))
    
    return prices