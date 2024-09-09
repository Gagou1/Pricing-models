We simulate option prices using various stochastic models. The option prices are computed with a Monte-Carlo pricer. 

**Black-Scholes model:** the stock prices $(S_t)$ are modelled by the following stochastic differential equation:
\begin{equation}
dS_t= rS_tdt+\sigma dW_t
\end{equation}
with $r,\sigma$ the constant rates and volatility and $W$ a Brownian motion

**Heston model:** This model also describes the volatility as a stochastic diffusion process, with driving Brownian motion correlated with the Brownian motion driving the stock prices:
```math
    \begin{cases}
      dS_t=rS_tdt+\sqrt{\nu_t}S_tdW^1_t\\
      d\nu_t=\kappa(\nu_b-\nu_t)+\epsilon\sqrt{\nu_t}(\rho dW^1_t+\sqrt{1-\rho^2dW^2_t})\\
    \end{cases}       
```

The Heston model is used in practice to correct the unrealistic hypothesis of constant/deterministic volatility in the Black-Scholes model.

Then, 
