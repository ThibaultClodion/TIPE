from AntColonyOptimization import Colony
from AStar import astar
import pygame as pg
import itertools
import time
import matplotlib.pyplot as plt


def get_position_of_node(matrix, node_type):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == node_type:
                return i, j


def get_position_list_of_foods(matrix):
    food_list = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "food":
                food_list.append((i, j))
    return food_list


def plot_test(test_name, executions_times, iterations):
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    plt.show()


def main(graphical_test=False):
    test_parameters = [
        {'name': '2 Points TSP [min_distance: 20, max_distance:25]',
         'points': 1,
         'min_distance': 20,
         'max_distance': 25},
        {'name': '5 Points TSP [min_distance: 20, max_distance:25]',
         'points': 4,
         'min_distance': 20,
         'max_distance': 25},
        {'name': '4 Points TSP [min_distance: 20, max_distance:25]',
         'points': 3,
         'min_distance': 20,
         'max_distance': 25},
        {'name': '5 Points TSP [min_distance: 10, max_distance:15]',
         'points': 4,
         'min_distance': 10,
         'max_distance': 15},
        {'name': '7 Points TSP [min_distance: 5, max_distance:10]',
         'points': 6,
         'min_distance': 5,
         'max_distance': 10}]

    for test_param in test_parameters:
        ant_colony = Colony(shouldPrint=False,
                            numFood=test_param['points'],
                            minFoodDistance=test_param['min_distance'],
                            maxFoodDistance=test_param['max_distance'])
        ant_colony.initField()
        ant_colony.createAnts()
        start_position = get_position_of_node(ant_colony.getMatrix(), "spawn")
        foods_position = get_position_list_of_foods(ant_colony.getMatrix())

        print(f"\nComparison Test ACO vs Bruteforce A* : {test_param['name']}")

        print("Starting ant colony optimization")
        time_start = time.time()

        running = True
        while running:
            if graphical_test:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                ant_colony.drawField()
            ant_colony.drawAndMoveAnts(should_draw=graphical_test)
            ant_colony.inc()
            if graphical_test:
                pg.display.flip()
            ant_colony.getClock().tick()
            ant_colony.globalEvaporate()
            if ant_colony.noFood():
                print("Ants have found the correct path in", ant_colony.getIterations(), "iterations.")
                running = False

        time_end = time.time()
        print(f"ACO completed in {time_end - time_start}")

        print("Starting Bruteforce A*")
        time_start = time.time()
        astar_paths = []
        all_points = foods_position + [start_position]
        all_possible_paths = itertools.permutations(all_points, len(all_points))
        for index, possible_path in enumerate(all_possible_paths):
            if index not in astar_paths:
                astar_paths.append([])
            for i in range(len(possible_path) - 1):
                if i not in astar_paths[index]:
                    astar_paths[index].append([])
                start_position = possible_path[i]
                end = possible_path[i + 1]
                astar_paths[index][i] = astar(ant_colony.getMatrix(), start_position, end)

        paths_length = []
        total_iterations = 0
        for index, path in enumerate(astar_paths):
            if index not in paths_length:
                paths_length.append({'id': index, 'cost': 0, 'iterations': 0})
            for point_path in path:
                paths_length[index]['cost'] += len(point_path[0])
                paths_length[index]['iterations'] += point_path[1]
                total_iterations += point_path[1]

        sorted_paths_length = sorted(paths_length, key=lambda d: d['cost'])
        shortest_path_data = sorted_paths_length[0]
        print(
            f"The shortest path found by bruteforce A* : {shortest_path_data} in {total_iterations} total iterations.")
        print(f"Path: {astar_paths[shortest_path_data['id']]}")
        time_end = time.time()
        print(f"Bruteforce A* completed in {time_end - time_start}")
        del ant_colony


if __name__ == '__main__':
    main(graphical_test=True)
