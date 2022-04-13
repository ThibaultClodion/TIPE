from DrawerHelper import *
from FunctionsSample import *
from metaheuristic.algortihms.ParticleSwarmOptimization import PSO

#function_to_execute = Functions2D.sin_max_in
function_to_execute = Functions3D.center
number_of_dimensions = 2
'''
if number_of_dimensions == 1:
    Functions2D.draw_function(function_to_execute)
else:
    Functions3D.draw_function(function_to_execute)
'''

x_min = -200
x_max = 200

model = PSO((x_min, x_max), (0, 0), function_to_execute, 20)
dHelper = DrawerHelper("Draw Function", 1200, 800)
if number_of_dimensions == 1:
    x_func, y_func = Functions2D.get_function_points(function_to_execute, x_min, x_max)
else:
    x_func, y_func = Functions3D.get_function_points(function_to_execute, (x_min, x_max))
xLag = 450
yLag = 150
while True:
    time.sleep(0.25)
    dHelper.draw_background(dHelper.BLACK)

    if number_of_dimensions == 1:
        for particule in model.X:
            dHelper.draw_point(dHelper.GREEN, (particule[0] + xLag, -function_to_execute(particule) + yLag), width=30)
        for i in range(len(x_func)):
            dHelper.draw_point(dHelper.BLUE, (x_func[i] + xLag, -y_func[i] + yLag))
    else:
        for i in range(len(x_func)):
            dHelper.draw_point(Functions3D.value_to_color(y_func[i]),
                               (x_func[i][0] + 250, -x_func[i][1] + 250))
        for particule in model.X:
            dHelper.draw_point(dHelper.BLUE, (particule[0], particule[1]), width=10)

    pygame.display.update()
    model.update_all_particule()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
