import numpy as np
import math
import random



class FellerErrorException(Exception):
    #Raise this exception if the Feller condition of the Heston model is not satisfied
    pass



class BlackScholesModel(object):

#dS_t=r*S_t*dt+sigma*S_t*dW_t

    def __init__(self, r, sigma, S0):
        self.r=r
        self.sigma=sigma
        self.S0=S0
        self.N=N
       
        
    def getRate(self):
        return self.r
    
        
        
    def createPath(self,steps,T,N):
        BScDiffusion=np.zeros((N,steps+1), dtype=float)
        BScDiffusion[:,0]=self.S0
        Vol=self.sigma*np.ones((N,steps+1),dtype=float)
        
        for j in range(1,steps+1):
            BScDiffusion[:,j]=(BScDiffusion[:,j-1]+BScDiffusion[:,j-1]*self.r*(T/steps)
                              +np.multiply(BScDiffusion[:,j-1],np.random.normal(size=N))*self.sigma*(math.sqrt(T)/math.sqrt(steps)))
        return [BScDiffusion,Vol]
    



class HestonModel(object):

#dS_t=r*S_t*dt+sqrt(v_t)*S_t*dW^1_t
#dv_t=kappa*(vb-v_t)*dt+epsilon*sqrt(v_t)*(rho*dW^1_t+sqrt(1-rho^2)dW^2_t)

    def __init__(self, r, kappa, v0, vb, epsilon, rho, S0):
        self.r=r
        self.kappa=kappa
        self.v0=v0
        self.vb=vb
        self.epsilon=epsilon
        self.rho=rho
        self.S0=S0
        
        try:
            if 2*self.kappa*self.vb<=self.epsilon**2:
                raise FellerErrorException
        except FellerErrorException:
            print('The Feller condition is not satisfied')
            
        
    def getRate(self):
        return self.r
    
    
       
    def __correlatedBrownian(self,steps,N):
        
        B1=np.random.normal(0,1,size=(N,steps))
        W=np.random.normal(0,1,(N,steps))
        B2=(self.rho)*B1+(np.sqrt(1-(self.rho)**2))*W
        return(B1,B2)
       
        
    def createPath(self,steps,T,N):
        HestDiffusion=np.zeros((N,steps+1), dtype=float)
        HestDiffusion[:,0]=self.S0
        Vol=np.zeros((N,steps+1), dtype=float)
        Vol[:,0]=self.v0
        B1=self.__correlatedBrownian(steps,N)[0]
        B2=self.__correlatedBrownian(steps,N)[1]
        #Generate the volatility
        
        for j in range(1,steps+1):
            Vol[:,j]=(Vol[:,j-1]+self.kappa*(self.vb*np.ones(N)-Vol[:,j-1])*(T/steps)
                    +self.epsilon*np.multiply(np.sqrt(np.maximum(Vol[:,j-1],np.zeros(N))),np.sqrt(T)/np.sqrt(steps)*B2[:,j-1]))
        #Generate the stock price
        
        for j in range(1,steps+1):
            HestDiffusion[:,j]=(HestDiffusion[:,j-1]+self.r*HestDiffusion[:,j-1]*(T/steps)
                             +np.multiply(np.sqrt(np.maximum(Vol[:,j-1],np.zeros(N))),np.multiply(HestDiffusion[:,j-1],B1[:,j-1])             *np.sqrt(T)/np.sqrt(steps)))
        return [HestDiffusion,np.sqrt(np.maximum(Vol,np.zeros((N,steps+1))))]
        