import numpy as np
import math




class Call(object):
    def __init__(self, K, T):
        
        self.K=K
        self.T=T
        
    def getTime(self):
        return self.T
    
        
    def payoff(self,path):
        lenght=len(path[0])
        return max(0,path[0][lenght-1]-self.K)
    

    
    
class Put(object):
    def __init__(self, K):
        self.K=K
        self.T=T
        
    def getTime(self):
        return self.T
        
    def payoff(self, path):
        lenght=len(path[0])
        return max(0,self.K-path[0][lenght-1])
    

    
class DOC(object):
    def __init__(self, K, L):
        self.K=K
        self.T=T
        self.L=L
        
    def getTime(self):
        return self.T

#Payoff of this option is given by (S_T-K)_+*I_{min_t(S_t)>L}
    def payoff(self, path):
        S=min(path[0])
        if S<self.L:
            return 0
        else:
            lenght=len(path[0])
            return max(0,path[0][lenght-1]-self.K)
    
class DOC_optimized(object):
    def __init__(self, K, L):
        self.K=K
        self.T=T
        self.L=L
        
    def getTime(self):
        return self.T

#Payoff of this option is given by (S_T-K)_+*I_{min_t(S_t)>L}
    def payoff(self, path):
        stock=path[0]
        Vol=path[1]
        pi=1
        disc=self.T/len(stock)
        for i in range(1,len(stock)):
            pi=pi*(1-np.exp(-max(stock[i]-self.L,0)*max(stock[i-1]-self.L,0)/(Vol[i-1]*disc)))
        lenght=len(stock)
        return pi*max(0,stock[lenght-1]-self.K)       