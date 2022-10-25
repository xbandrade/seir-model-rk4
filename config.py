# DEFAULT VALUES
BETA = 2.5 * (1 / 5.6)  # Infection rate
POPULATION = 632 * 632  # Total population in the model
DAYS = 400  # Days of simulations
NATURAL_DEATH = 3.424657534e-5  # Natural death rate
RECOVERY_RATE = 1 / 12  # Recovery/discharge rate
DISEASE_DEATH = .02  # Disease death rate
EXP_TO_INFECTIOUS = 1 / 14  # Probability to go from Exposed to Infectious
E_0 = 5  # Exposed at t=0
I_0 = 0  # Infectious at t=0
R_0 = 0  # Recovered at t=0
S_0 = POPULATION - E_0 - I_0 - R_0  # Susceptible at t=0
T_0 = 0  # Initial time