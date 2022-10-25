# SEIR Model RK4

SEIR Model solved by fourth order Runge-Kutta Method (RK4)

### Compartments:
> S - Individuals susceptible to contagion<br/>
> E - Individuals exposed to the pathogen<br/>
> I - Individuals who can transmit the disease<br/>
> R - Individuals recovered from disease<br/>

### ➡️ Run:
**python -m seir**

###  Parameters:
>  β - Transmission rate<br/>
>  γ - Recovery/discharge rate<br/>
>  μ - Natural death rate<br/>
>  α - Probability to become infectious after being exposed<br/>
>  ε - Death by disease rate<br/>

#### Default parameters adapted from [Agent-Based Model for COVID-19](https://github.com/xbandrade/covidABM).
