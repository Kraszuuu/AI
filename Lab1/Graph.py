import Node
from heapq import heappush, heappop
from datetime import datetime, timedelta
from math import radians, sin, cos, atan2, sqrt
AVG_SPEED = 8

class Graph:
    def __init__(self) -> None:
        self.nodes = set()

    #adds node to set
    def work_on_node(self, name : str, latitude : float, longitude : float) -> Node:
        for node in self.nodes:
            if node.name == name:
                node.recalculate_coordinates(latitude, longitude)
                return node
        node = Node.Node(name, latitude, longitude)
        self.nodes.add(node)
        return node
    
    def euclidean_distance(self, node1, node2):
        # Calculate Euclidean distance between two nodes based on their coordinates
        return ((float(node1.latitude)) - float(node2.latitude)) ** 2 + (float(node1.longitude) - float(node2.longitude) ** 2) ** 0.5

    def find_node_from_name(self, node_name):
        for element in self.nodes:
            if element.name == node_name:
                return element
        raise ObjectNotFoundError(f'Node of name {node_name} not found in the set')
    
    def time_string_to_int(time):
        time = time.split(":")
        return int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])

    def generate_schedule(self, end_node, previous_node, previous_line, previous_departure_time):
        schedule = []
        current_node = end_node
        while current_node:
            previous = previous_node[current_node]
            if previous:
                schedule.insert(0, (previous_line[current_node], previous_departure_time[current_node], previous.name))
            current_node = previous
        return schedule
        
    def dijkstra(self, start_node, end_node, start_time):
        def compare_distances(tuple):
            return tuple[0]
        
        start_time = self.time_string_to_int(start_time)
        start_node = self.find_node_from_name(start_node)
        end_node = self.find_node_from_name(end_node)
        # Initialize distances to infinity for all nodes
        distances_from_start = {node: float('inf') for node in self.nodes}
        distances_from_start[start_node] = 0

        # Priority queue to keep track of nodes to visit
        priority_queue = [(0, start_node)]

        # Dictionary to track the previous node and line for each node
        previous_node = {node: None for node in self.nodes}
        previous_line = {node: None for node in self.nodes}
        previous_departure_time = {node: None for node in self.nodes}

        #which nodes were visited
        visited = set()

        # Start time of computation
        start_time_computation = datetime.now()

        while priority_queue:
            current_distance, current_node = heappop(priority_queue)

            # If the current node is the end node, we can stop
            if current_node == end_node:
                break

            for neighbor, edges in current_node.connections.items():
                if (neighbor not in visited):
                    for edge in edges:
                        if self.time_string_to_int(edge.departure_time) >= start_time + int(current_distance):
                            travel_time = self.time_string_to_int(edge.arrival_time) - start_time
                            if travel_time < distances_from_start[neighbor]:
                                distances_from_start[neighbor] = travel_time
                                neighbor.parent = current_node
                                neighbor.used_line = edge.line
                                priority_queue.insert(0, (travel_time, neighbor))
                                priority_queue.sort(key=compare_distances)
                                previous_node[neighbor] = current_node
                                previous_line[neighbor] = edge.line
                                previous_departure_time[neighbor] = edge.departure_time
                                break
            visited.add(current_node)

        # Compute total time taken for computation
        end_time_computation = datetime.now()
        computation_time = (end_time_computation - start_time_computation).total_seconds()

        # Generate schedule
        schedule = self.generate_schedule(end_node, previous_node, previous_line, previous_departure_time)

        return distances_from_start[end_node], computation_time, schedule, len(visited)
    
    def astar(self, start_node, end_node, start_time, criterion='t'):
        def compare_distances(tuple):
            return tuple[2], tuple[0]
        #based on Haversine formula
        def calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude):
            radius = 6371000
            start_latitude = radians(start_latitude)
            start_longitude = radians(start_longitude)
            end_latitude = radians(end_latitude)
            end_longitude = radians(end_longitude)
            d_lat = start_latitude - end_latitude
            d_lon = start_longitude - end_longitude
            a = sin(d_lat / 2)**2 + cos(start_latitude) * cos(end_latitude) * sin(d_lon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = radius * c
            return distance
        
        start_time = self.time_string_to_int(start_time)
        start_node = self.find_node_from_name(start_node)
        end_node = self.find_node_from_name(end_node)

        # Priority queue to keep track of nodes to visit
        priority_queue = [(0, start_node, 0)]

        # Dictionary to track the previous node and line for each node
        previous_node = {node: None for node in self.nodes}
        previous_line = {node: None for node in self.nodes}
        previous_departure_time = {node: None for node in self.nodes}
        distance_traveled = {node : None for node in self.nodes}
        distance_to_cover = {node : float('inf') for node in self.nodes}
        distance_traveled[start_node] = 0
        distance_to_cover[start_node] = calculate_distance(float(start_node.latitude), float(start_node.longitude), float(end_node.latitude), float(end_node.longitude))
        total_distance = {node : float('inf') for node in self.nodes}
        total_time = {node: float('inf') for node in self.nodes}
        total_time[start_node] = 0


        #which nodes were visited
        visited = set()

        # Start time of computation
        start_time_computation = datetime.now()

        while priority_queue:
            current_travel_time, current_node, current_travel_distance = heappop(priority_queue)

            # If the current node is the end node, we can stop
            if current_node == end_node:
                break

            for neighbor, edges in current_node.connections.items():
                print(current_node.name + " " + neighbor.name)
                if (neighbor not in visited):
                    neighbor_distance_to_cover = calculate_distance(float(end_node.latitude), float(end_node.longitude), float(neighbor.latitude), float(neighbor.longitude))
                    neighbor_distance_traveled = distance_traveled[current_node] + calculate_distance(float(current_node.latitude), float(current_node.longitude), float(neighbor.latitude), float(neighbor.longitude))
                    neighbor_total_distance = neighbor_distance_traveled + neighbor_distance_to_cover
                    if neighbor_total_distance < total_distance[neighbor]:
                        for edge in edges:
                            if self.time_string_to_int(edge.departure_time) >= start_time + int(current_travel_time):
                                total_time[neighbor] = self.time_string_to_int(edge.arrival_time) - start_time
                                total_distance[neighbor] = neighbor_total_distance
                                distance_to_cover[neighbor] = neighbor_distance_to_cover
                                distance_traveled[neighbor] = neighbor_distance_traveled
                                neighbor.parent = current_node
                                neighbor.used_line = edge.line
                                priority_queue.insert(0, (total_time[neighbor], neighbor, neighbor_total_distance))
                                priority_queue.sort(key=compare_distances)
                                previous_node[neighbor] = current_node
                                previous_line[neighbor] = edge.line
                                previous_departure_time[neighbor] = edge.departure_time
                                break
            visited.add(current_node)

        # Compute total time taken for computation
        end_time_computation = datetime.now()
        computation_time = (end_time_computation - start_time_computation).total_seconds()

        # Generate schedule
        schedule = self.generate_schedule(end_node, previous_node, previous_line, previous_departure_time)

        return total_time[end_node], computation_time, schedule, len(visited)

    def calculate_travel_time(self, start_time, arrival_time_neighbor):
        return self.time_string_to_int(arrival_time_neighbor) - self.time_string_to_int(start_time)

class ObjectNotFoundError(Exception):
    pass

class CriterionError(Exception):
    pass