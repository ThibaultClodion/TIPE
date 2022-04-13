from DrawerHelper import *
import math


class Functions2D:
    @staticmethod
    def linear_then_const(x):
        if x[0] >= 20:
            return 15
        else:
            return x[0]

    @staticmethod
    def up_and_down(x, center_in=40):
        if x[0] > center_in:
            return center_in - (x[0] - center_in)
        else:
            return x[0]

    @staticmethod
    def sin_max_in(x, max_in=100):
        coeff = 100
        return math.sin(x[0] / 100) * coeff

    @staticmethod
    def draw_function(function, x_min=-200, x_max=200):
        dHelper = DrawerHelper("Draw Function", 500, 500)
        while True:
            for x in range(x_min, x_max):
                y = function([x])
                dHelper.draw_point(dHelper.BLUE, (x + 150, -y + 100))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

    @staticmethod
    def get_function_points(function, x_min=-200, x_max=200):
        x_res = []
        y_res = []
        for x in range(x_min, x_max):
            x_res.append(x)
            y_res.append(function([x]))
        return x_res, y_res


class Functions3D:
    @staticmethod
    def center(x, center_values=(200, 200)):
        x_ecart = abs(x[0] - center_values[0])
        y_ecart = abs(x[1] - center_values[1])
        return 500 - x_ecart - y_ecart

    @staticmethod
    def value_to_color(res):
        if res >= 400:
            return 255, 0, 0
        elif 250 < res < 400:
            return 255, 122, 0
        elif 100 < res < 250:
            return 255, 255, 0
        else:
            return 0, 255, 0

    @staticmethod
    def get_function_points(function, x=(-200, 200), y=(-200, 200)):
        x_res = []
        y_res = []
        for x_value in range(x[0], x[1]):
            for y_value in range(y[0], y[1]):
                x_res.append([x_value, y_value])
                y_res.append(function([x_value, y_value]))
        return x_res, y_res

    @staticmethod
    def draw_function(function, min_values=(-200, -200), max_values=(200, 200)):
        dHelper = DrawerHelper("Draw Function", 500, 500)
        while True:
            for x in range(min_values[0], max_values[0]):
                for y in range(min_values[1], max_values[1]):
                    result = function([x, y])
                    dHelper.draw_point(Functions3D.value_to_color(result), (x + 250, -y + 250))
                    '''
                    if result >= 400:
                        dHelper.draw_point(dHelper.RED, (x + 250, -y + 250))
                    elif 250 < result < 400:
                        dHelper.draw_point(dHelper.ORANGE, (x + 250, -y + 250))
                    '''
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()