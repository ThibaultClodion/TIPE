import numpy as np
import time
from DrawerHelper import *
from FunctionsSample import *


class NaiveLocalSearch:
    def __init__(self, f, min_values=None, max_values=None):
        assert (len(min_values) == len(max_values))
        assert (min_values is not None)
        assert (max_values is not None)
        self.f = f
        self.min_values = min_values
        self.max_values = max_values
        self.best_values = None
        self.best_result = None

    def execute(self, it_max=1000):
        it = 0
        while it < it_max:
            self.update_and_apply()
            it += 1
        return self.best_values

    def update(self):
        x = [np.array((self.max_values[0] - self.min_values[0]) * np.random.random_sample(1) + self.min_values[0])]
        for i in range(1, len(self.min_values)):
            x = np.concatenate((x, (self.max_values[i] - self.min_values[i]) * np.random.random_sample(1) + self.min_values[i]), axis=1)
        return x

    def update_and_apply(self):
        x = self.update()
        result = self.f(x)
        if self.best_values is None or result > self.best_result:
            self.best_result = result
            self.best_values = x


# add method set parameters
function_to_execute = Functions2D.up_and_down
# Functions2D.draw_function(function_to_execute)

model = NaiveLocalSearch(function_to_execute, [-40], [120])

dHelper = DrawerHelper("Draw Function", 500, 500)
x_func, y_func = Functions2D.get_function_points(function_to_execute)
xLag = 150
yLag = 100
while True:
    time.sleep(0.25)
    dHelper.draw_background(dHelper.WHITE)
    if model.best_values is not None:
        dHelper.draw_point(dHelper.GREEN, (model.best_values[0] + xLag, -function_to_execute(model.best_values) + yLag), width=100)
    for i in range(len(x_func)):
        dHelper.draw_point(dHelper.BLUE, (x_func[i] + xLag, -y_func[i] + yLag))

    pygame.display.update()
    model.update_and_apply()
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
