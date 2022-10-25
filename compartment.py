from config import *


def reset_comp(compartments):
    """Resets plot lists and populations to default"""
    s, e, i, r = compartments
    s.plot_list, e.plot_list, i.plot_list, r.plot_list = [], [], [], []
    s.pop = S_0
    e.pop = E_0
    i.pop = I_0
    r.pop = R_0
    return s, e, i, r


class Compartment:
    def __init__(self, pop=0) -> None:
        self.N = POPULATION  # Total population in the model
        self.pop = pop  # Population in the compartment
        self.name = 'Generic Compartment'  # Name of the compartment
        self.beta = BETA  # Infection rate
        self.mu = NATURAL_DEATH  # Natural death rate
        self.epsilon = DISEASE_DEATH  # Disease death rate
        self.gamma = RECOVERY_RATE  # Recovery/discharge rate
        self.alpha = EXP_TO_INFECTIOUS  # Probability to go from exposed to infectious
        self.plot_list = []

    def __str__(self) -> str:
        return f'{self.name}: {self.pop}\n'

    def __float__(self) -> float:
        return float(self.pop)


class S(Compartment):
    def __init__(self, pop=0) -> None:
        super().__init__(pop)
        self.name = 'Susceptible'

    def f(self, t, s_i, e_i, i_i, r_i) -> float:
        return self.mu * (self.N - s_i) - self.beta * s_i * i_i / self.N


class E(Compartment):
    def __init__(self, pop=0) -> None:
        super().__init__(pop)
        self.name = 'Exposed'

    def f(self, t, s_i, e_i, i_i, r_i) -> float:
        return self.beta * s_i * i_i / self.N - (self.mu + self.alpha) * e_i


class I(Compartment):
    def __init__(self, pop=0) -> None:
        super().__init__(pop)
        self.name = 'Infectious'

    def f(self, t, s_i, e_i, i_i, r_i) -> float:
        return self.alpha * e_i - (self.mu + self.epsilon + self.gamma) * i_i


class R(Compartment):
    def __init__(self, pop=0) -> None:
        super().__init__(pop)
        self.name = 'Recovered'
    
    def f(self, t, s_i, e_i, i_i, r_i) -> float:
        return self.gamma * i_i - self.mu * r_i