import time
from DrawerHelper import *
from FunctionsSample import *
from metaheuristic.algortihms.ParticleSwarmOptimization import PSO
from metaheuristic.algortihms.NaiveLocalSearch import NaiveLocalSearch

# adapter le code a tous les algos
# trouver des fonctions complexes
# pouvoir afficher n'importe quelle type de functions correctement

function_to_execute = Functions2D.sin_max_in
# Functions2D.draw_function(function_to_execute)

x_min = -600
x_max = 600

model = PSO((x_min, x_max), (0, 0), function_to_execute, 1, 20)
dHelper = DrawerHelper("Draw Function", 1200, 800)
x_func, y_func = Functions2D.get_function_points(function_to_execute, x_min, x_max)

xLag = 450
yLag = 150
while True:
    time.sleep(0.25)
    dHelper.draw_background(dHelper.BLACK)
    for particule in model.X:
        dHelper.draw_point(dHelper.GREEN, (particule[0] + xLag, -function_to_execute(particule) + yLag), width=30)
    for i in range(len(x_func)):
        dHelper.draw_point(dHelper.BLUE, (x_func[i] + xLag, -y_func[i] + yLag))

    pygame.display.update()
    model.update_all_particule()
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