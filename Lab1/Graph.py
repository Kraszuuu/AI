import Node
from heapq import heappush, heappop
from datetime import datetime, timedelta
from math import radians, sin, cos, atan2, sqrt
AVG_SPEED = 4

class Graph:
    def __init__(self) -> None:
        self.nodes = set()
        self.lines = dict()

    #adds node to set
    def work_on_node(self, name : str, latitude : float, longitude : float) -> Node:
        for node in self.nodes:
            if node.name == name:
                node.recalculate_coordinates(latitude, longitude)
                return node
        node = Node.Node(name, latitude, longitude)
        self.nodes.add(node)
        return node
    
    def work_on_line(self, line : str, start_node : Node, end_node : Node):
        if line not in self.lines:
            self.lines[line] = [start_node, end_node]
            # self.lines.update(line, [start_node, end_node])
            return
        current_line : list = self.lines.get(line)
        if start_node not in current_line: current_line.append(start_node)
        if end_node not in current_line: current_line.append(end_node)
    
    def find_node_from_name(self, node_name):
        for element in self.nodes:
            if element.name == node_name:
                return element
        raise ObjectNotFoundError(f'Node of name {node_name} not found in the set')
    
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
        
        start_time = time_string_to_int(start_time)
        start_node = self.find_node_from_name(start_node)
        end_node = self.find_node_from_name(end_node)
        # Initialize distances to infinity for all nodes
        times_from_start = {node: float('inf') for node in self.nodes}
        times_from_start[start_node] = 0

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
            if current_node == end_node: break

            for neighbor, edges in current_node.connections.items():
                if (neighbor in visited): continue
                for edge in edges:
                    if time_string_to_int(edge.departure_time) < start_time + int(current_distance): continue
                    neighbor_travel_time = time_string_to_int(edge.arrival_time) - start_time
                    if neighbor_travel_time >= times_from_start[neighbor]: continue
                    times_from_start[neighbor] = neighbor_travel_time
                    priority_queue.insert(0, (neighbor_travel_time, neighbor))
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

        return times_from_start[end_node], computation_time, schedule, len(visited)
    
    def astar(self, start_node, end_node, start_time, criterion='t'):
        def compare_distances(tuple):
            if criterion == 't': return tuple[2], tuple[0]
            elif criterion == 'p': pass ################################
        
        def calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude):
            lat_diff = abs(float(start_latitude) - float(end_latitude)) * 111000
            lon_diff = abs(float(start_longitude) - float(end_longitude)) * 111000
            result = (lat_diff ** 2 + lon_diff ** 2) ** 0.5
            return result
        
        def get_used_lanes(node) -> list:
            result = list()
            for neighbor, edges in node.connections.items():
                for edge in edges:
                    if edge.line not in result:
                        result.append(edge.line)
            return result
                
        def estimate_time_between_points(start_latitude, start_longitude, end_latitude, end_longitude):
            result = calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude) / AVG_SPEED
            return result
        
        start_time = time_string_to_int(start_time)
        start_node = self.find_node_from_name(start_node)
        end_node = self.find_node_from_name(end_node)

        visited = set()
        previous_node = {node: None for node in self.nodes}
        previous_line = {node: None for node in self.nodes}
        previous_departure_time = {node: None for node in self.nodes}

        start_time_computation = datetime.now()
        if (criterion == 't'):
            times_from_start = {node: float('inf') for node in self.nodes}
            times_to_end_est = {node : float('inf') for node in self.nodes}
            times_from_start[start_node] = 0.0
            times_to_end_est[start_node] = estimate_time_between_points(start_node.latitude, start_node.longitude, end_node.latitude, end_node.longitude)
            total_times = {node : times_from_start[node] + times_to_end_est[node] for node in self.nodes}

            #time_from_start, name, total_time_to_end(est)
            priority_queue = [(times_from_start[start_node], start_node, total_times[start_node])]
            while priority_queue:
                current_travel_time, current_node, current_total_time = heappop(priority_queue)

                if current_node == end_node: break
                for neighbor, edges in current_node.connections.items():
                    if(neighbor in visited): continue
                    check_line_param = False
                    for edge in edges:
                        edge_departure = time_string_to_int(edge.departure_time)
                        if (check_line_param):
                            if(time_string_to_int(previous_departure_time[neighbor]) < edge_departure): break
                            if(edge.line != previous_line[current_node]): continue
                        if(edge_departure < start_time + times_from_start[current_node]): continue
                        neighbor_from_start =  time_string_to_int(edge.arrival_time) - start_time
                        neighbor_to_end = estimate_time_between_points(neighbor.latitude, neighbor.longitude, end_node.latitude, end_node.longitude)
                        neighbor_total_time = neighbor_from_start + neighbor_to_end
                        if(neighbor_total_time >= total_times[neighbor]): continue
                        total_times[neighbor] = neighbor_total_time
                        times_from_start[neighbor] = neighbor_from_start
                        times_to_end_est[neighbor] = neighbor_to_end
                        priority_queue.insert(0, (neighbor_from_start, neighbor, neighbor_total_time))
                        priority_queue.sort(key=compare_distances)
                        previous_node[neighbor] = current_node
                        previous_line[neighbor] = edge.line
                        previous_departure_time[neighbor] = edge.departure_time
                        check_line_param = True
                        # break
                visited.add(current_node)
        # elif (criterion == 'p'):
        #     pass
            # #amount of transfers needed to use this line
            # amount_of_transfers = list()
            # #distance to an end
            # distance_to_end = {node : int('inf') for node in self.nodes}
            # #lowest cost of getting to the stop
            # cost_to_get = {node : int('inf') for node in self.nodes}
            # #previous node
            # previous_node = {node : None for node in self.nodes}
            # #best lane
            # best_lane = {node : list() for node in self.nodes}

            # distance_to_end[start_node] = calculate_distance(start_node.latitude, start_node.longitude, end_node.latitude, end_node.longitude)
            # cost_to_get[start_node] = 0
            # help_list = get_used_lanes(start_node)
            # amount_of_transfers.append(help_list)
            # amount_of_transfers.append([])
            # amount_of_transfers.append([])
            # amount_of_transfers.append([])
            # amount_of_transfers.append([])
            # amount_of_transfers.append([])
            # amount_of_transfers.append([])

            # # node, cost_to_get, distance_to_end
            # priority_queue = [(start_node, cost_to_get[start_node], distance_to_end[start_node])]

            # while priority_queue:
            #     current_node, current_used_lanes, current_distance_to_end = heappop(priority_queue)

            #     if current_node == end_node: break
            #     for neighbor, edges in current_node.connections.items():
            #         if neighbor in visited: continue
            #         edge_cost = cost_to_get[current_node]
            #         cost_to_get[neighbor] = edge_cost + 1
            #         for edge in edges:
            #             if edge.line in amount_of_transfers[edge_cost]: cost_to_get[neighbor] = edge_cost
            #             else: 
            #                 if edge.line not in amount_of_transfers[edge_cost+1]: amount_of_transfers[edge_cost+1].append(edge.line)
            
        else: raise CriterionError("Wrong criterion given")
                    
                    
        # Compute total time taken for computation
        end_time_computation = datetime.now()
        computation_time = (end_time_computation - start_time_computation).total_seconds()

        # Generate schedule
        schedule = self.generate_schedule(end_node, previous_node, previous_line, previous_departure_time)
        return total_times[end_node], computation_time, schedule, len(visited)

    def calculate_travel_time(self, start_time, arrival_time_neighbor):
        return time_string_to_int(arrival_time_neighbor) - time_string_to_int(start_time)
    
    def create_edges_dict(self):
        result = dict()
        for node, edges in self.nodes.items():
            for edge in self.edges:
                if edge.line not in result:
                    result.update({edge.line : int('inf')})
        return result
    
    def print_lines(self):
        for key, values in self.lines.items():
            print(key)
            for value in values:
                print("\t"+value.name)

def time_string_to_int(time):
    time = time.split(":")
    return int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])

class ObjectNotFoundError(Exception):
    pass

class CriterionError(Exception):
    pass