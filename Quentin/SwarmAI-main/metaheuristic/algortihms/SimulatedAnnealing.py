import numpy as np
import time
from DrawerHelper import *
from FunctionsSample import *


class SimulatedAnnealing:
    def __init__(self, f, min_values=None, max_values=None, temperature=5, stagnation=0):
        assert (len(min_values) == len(max_values))
        assert (min_values is not None)
        assert (max_values is not None)
        self.f = f
        self.min_values = min_values
        self.max_values = max_values
        self.best_values = None
        self.best_result = None
        self.real_best_result = None
        self.temperature = temperature
        self.initial_temperature = self.temperature
        self.stagnation = stagnation
        self.initial_stagnation = self.stagnation
        self.limit = 500
        self.previous_error = None

    def metropolis_criterium(self, current_result):
        if self.temperature <= 0:
            return 0 if current_result - self.best_result <= 0 else 1
        return math.exp((current_result - self.best_result) / self.temperature)

    def init(self):
        x = self.random_values()
        self.best_values = x
        self.best_result = self.f(x)
        self.previous_error = self.best_values

    def execute(self, it_max=1000):
        it = 1
        self.init()
        while it < it_max:
            self.update_and_apply()
            it += 1
        return self.best_values

    def random_values(self):
        x = [np.array((self.max_values[0] - self.min_values[0]) * np.random.random_sample(1) + self.min_values[0])]
        for i in range(1, len(self.min_values)):
            x = np.concatenate((x, (self.max_values[i] - self.min_values[i]) * np.random.random_sample(1) + self.min_values[i]), axis=1)
        return x

    def update(self):
        x = self.random_values()
        if np.random.random_sample(1) <= self.metropolis_criterium(self.f(x)):
            self.best_result = self.f(x)
            self.best_values = x
            if self.real_best_result is None or self.best_result > self.real_best_result:
                self.real_best_result = self.best_result

    def update_and_apply(self):
        model.update()
        if self.previous_error == self.best_values:
            self.stagnation = self.stagnation + 1
            if self.stagnation > self.limit:
                self.temperature = self.initial_temperature
                self.stagnation = self.initial_stagnation
        else:
            self.stagnation = self.initial_stagnation

        self.temperature = self.temperature * 0.999
        self.temperature = max(self.temperature, 0)
        self.previous_error = self.best_values


# add method set parameters
function_to_execute = Functions2D.up_and_down
# Functions2D.draw_function(function_to_execute)

model = SimulatedAnnealing(function_to_execute, [-40], [120])

dHelper = DrawerHelper("Draw Function", 500, 500)
x_func, y_func = Functions2D.get_function_points(function_to_execute)
xLag = 150
yLag = 100
model.init()
while True:
    time.sleep(0.25)
    dHelper.draw_background(dHelper.WHITE)
    if model.best_values is not None:
        dHelper.draw_point(dHelper.GREEN, (model.best_values[0] + xLag, -function_to_execute(model.best_values) + yLag), width=100)
    for i in range(len(x_func)):
        dHelper.draw_point(dHelper.BLUE, (x_func[i] + xLag, -y_func[i] + yLag))

    pygame.display.update()
    model.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

'''
start = time.time()
best_position = model.execute(X, V, function_to_execute)
end = time.time()
elapsed = end - start
print(f'Temps d\'exécution : {elapsed:.5}ms')
# https://www.ukonline.be/cours/python/opti/chapitre3-1#:~:text=Une%20autre%20possibilit%C3%A9%20pour%20mesurer,fonction%20time%20du%20module%20time%20.

print(best_position)
print(function_to_execute(best_position))
'''
