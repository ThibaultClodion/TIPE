import numpy as np


def init_data_between(data_min, data_max, number_of_particules, number_of_dimensions):
    return (data_max - data_min) * np.random.random_sample(
        (number_of_particules, number_of_dimensions)) + data_min  # [v_min, v_max]


class PSO:
    def __init__(self, X, V, f, number_of_dimensions, number_of_particules=20):
        self.number_of_particules = number_of_particules
        self.X = init_data_between(X[0], X[1], self.number_of_particules, number_of_dimensions)
        self.V = init_data_between(V[0], V[1], self.number_of_particules, number_of_dimensions)
        self.f = f
        self.P = np.copy(self.X)
        self.Pg = np.copy(self.P[np.argmax([self.f(x) for x in self.P])])

    def execute(self, it_max=100, omega=1.0, acceleration_coeff1=1.0, acceleration_coeff2=1.0):
        it = 0
        while it < it_max:
            self.update_all_particule(omega, acceleration_coeff1, acceleration_coeff2)
            it += 1
        return self.Pg

    def update_all_particule(self, omega=0.0, acceleration_coeff1=1.0, acceleration_coeff2=1.0):
        for i in range(len(self.X)):
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()
            self.V[i] = omega * self.V[i] + acceleration_coeff1 * r1 * (self.P[i] - self.X[i]) \
                        + acceleration_coeff2 * r2 * (self.Pg - self.X[i])
            self.X[i] = self.V[i] + self.X[i]
            if self.f(self.X[i]) > self.f(self.P[i]):
                self.P[i] = np.copy(self.X[i])
                if self.f(self.X[i]) > self.f(self.Pg):
                    self.Pg = np.copy(self.X[i])