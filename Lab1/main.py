from collections import deque
import csv
from datetime import datetime
import time
import Node, Edge, Graph
import math
FILE_PATH = "Lab1\connection_graph.csv"
            
def load_data_from_csv(filename):
    graph = Graph.Graph()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        i = 0
        next(reader)
        for row in reader:
            start_node = graph.work_on_node(row[5], row[7], row[8])
            end_node = graph.work_on_node(row[6], row[9], row[10])
            start_node.work_on_end_node(end_node)
            start_node.work_on_connection(end_node, row[0], row[2], row[3], row[4])
            i += 1
            # if (i == 10000): break
    return graph   

def build_graph() -> Graph.Graph:
    start_time = time.time()
    graph = load_data_from_csv(FILE_PATH)
    # for elem in graph.nodes:
    #     print("Poczatek: " + elem.to_string())
    #     for elem2 in elem.connections:
    #         print(" Koniec: " + elem2.to_string())
    #         print("     Polaczenia: ")
    #         elem.print_connections(elem2)
    end_time = time.time()
    execution_time = end_time - start_time
    print("Czas budowania grafu: ", execution_time)
    return graph

def print_results(shortest_distance, computation_time, schedule, visited):
    previous_line = None
    for line, departure_time, stop_name in schedule:
        if(previous_line != line):
            previous_line = line
            print(f"Line: {line}, Departure Time: {departure_time}, Stop: {stop_name}")
    # Print shortest distance and computation time
    print("Visited nodes:", visited)
    print("Shortest distance:", shortest_distance, "s")
    print("Computation time:", computation_time)
    print("=================================================================")
    

def dijkstra_tests():
    def test1():
        shortest_distance, computation_time, schedule, visited = graph.dijkstra("KROMERA", "Katedra", "21:15:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test2():
        shortest_distance, computation_time, schedule, visited = graph.dijkstra("KROMERA", "FAT", "21:15:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test3():
        shortest_distance, computation_time, schedule, visited = graph.dijkstra("Daszyńskiego", "Inowrocławska", "22:55:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test4():
        shortest_distance, computation_time, schedule, visited = graph.dijkstra("Nowowiejska", "ROD Zgoda", "12:55:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test5():
        shortest_distance, computation_time, schedule, visited = graph.dijkstra("Warmińska", "WOJNÓW (pętla)", "11:00:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    dijkstra_time_start = time.time()
    test1()
    test2()
    test3()
    test4()
    test5()
    dijkstra_time_end = time.time()
    total_dijkstra_time = dijkstra_time_end - dijkstra_time_start
    print("*******************************************************************")
    print(f'Total dijkstra time: {total_dijkstra_time}')
    print("*******************************************************************")

def astar_tests():
    def test1():
        shortest_distance, computation_time, schedule, visited = graph.astar("KROMERA", "Katedra", "21:15:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test2():
        shortest_distance, computation_time, schedule, visited = graph.astar("KROMERA", "FAT", "21:15:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test3():
        shortest_distance, computation_time, schedule, visited = graph.astar("Daszyńskiego", "Inowrocławska", "22:55:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test4():
        shortest_distance, computation_time, schedule, visited = graph.astar("Nowowiejska", "ROD Zgoda", "12:55:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    def test5():
        shortest_distance, computation_time, schedule, visited = graph.astar("Warmińska", "WOJNÓW (pętla)", "11:00:00")
        print_results(shortest_distance, computation_time, schedule, visited)

    astar_time_start = time.time()
    test1()
    test2()
    test3()
    test4()
    test5()
    astar_time_end = time.time()
    total_astar_time = astar_time_end - astar_time_start
    print("*******************************************************************")
    print(f'Total A* time: {total_astar_time}')
    print("*******************************************************************")

graph = build_graph()
dijkstra_tests()
astar_tests()