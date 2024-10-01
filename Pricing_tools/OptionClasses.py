import numpy as np
import math




class Call(object):
    def __init__(self, K, T):
        
        self.K=K
        self.T=T
        
    def getTime(self):
        return self.T
    
        
    def payoff(self,path):
        length=len(path[0][0,:])
        n_paths=len(path[0])
        return np.maximum(np.zeros(n_paths),path[0][:,length-1]-self.K*np.ones(n_paths))
    

    
    
class Put(object):
    def __init__(self, K, T):
        self.K=K
        self.T=T
        
    def getTime(self):
        return self.T
        
    def payoff(self, path):
        length=len(path[0][0,:])
        n_paths=len(path[0])
        return np.maximum(np.zeros(n_paths),self.K*np.ones(n_paths)-path[0][:,length-1])
    

    
class DOC(object):
    def __init__(self, K, L, T):
        self.K=K
        self.L=L
        self.T=T
        
    def getTime(self):
        return self.T

#Payoff of this option is given by (S_T-K)_+*I_{min_t(S_t)>L}
    def payoff(self, path):
        length=len(path[0][0,:])
        n_paths=len(path[0])
        S=np.min(path[0],axis=1)
        sgn=(np.sign(S-L*np.ones(n_paths))+1)/2
        return np.multiply(np.maximum(np.zeros(n_paths),path[0][:,length-1]-self.K*np.ones(n_paths)),sgn)
    
class DOCOptimized(object):
    def __init__(self, K, L, T):
        self.K=K
        self.L=L
        self.T=T
        
    def getTime(self):
        return self.T

#Payoff of this option is given by (S_T-K)_+*I_{min_t(S_t)>L}
    def payoff(self, path):
        stock=path[0]
        Vol=path[1]
        length=len(path[0][0,:])
        n_paths=len(path[0])
        P=np.ones((n_paths,length))
        disc=self.T/length
        for i in range(1,length):
            P[:,i]=P[:,i-1]*(np.ones(n_paths)-np.exp(np.divide(-2*np.multiply(np.maximum(path[0][:,i]-self.L*np.ones(n_paths),np.zeros(n_paths)),np.maximum(path[0][:,i-1]-self.L*np.ones(n_paths),np.zeros(n_paths))),disc*np.multiply(np.maximum(path[1][:,i-1],0.0001*np.ones(n_paths))**2,path[0][:,i-1]**2))))
        
        return np.multiply(P[:,length-1],np.maximum(np.zeros(n_paths),path[0][:,length-1]-self.K*np.ones(n_paths)))    
    
    