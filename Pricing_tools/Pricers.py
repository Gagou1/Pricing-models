import numpy as np
import math
import random



#Monte Carlo pricer giving option prices (option table options) using the model model, simulated with steps steps and N paths.
def MonteCarloPricer(model, options, steps, N):
    #options is an array that contains options objects stored in array whose first axis is time index
    rate  = model.getRate()
    Times = np.zeros_like(options)
    for index in np.ndindex(options.shape):
        Times[index] = options[index].getTime()
    
    #get the maximum time in order to compute the total number of discretization steps
    maxT     = np.amax(Times)
    
    #Compute the exponential discount factor
    discount = np.zeros_like(options)
    for index in np.ndindex(options.shape):
        discount[index]=np.exp(-rate*Times[index])
        
    #Create the N-dimensional paths
    path   = model.createPath(steps,maxT,N)
    
    #Compute the prices
    prices = np.zeros_like(options)
    for index in np.ndindex(options.shape):
        prices[index]=(discount[index])*np.mean(options[index].payoff([path[0][:,0:math.floor(steps*Times[index]/maxT)+1],path[1][:,0:math.floor(steps*Times[index]/maxT)+1]]))
    
    return prices