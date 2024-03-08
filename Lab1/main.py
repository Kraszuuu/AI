from collections import deque
import csv
from datetime import datetime
import time
FILE_PATH = "Lab1\connection_graph.csv"

class Node:
    def __init__(self, name : str) -> None:
        self.name : str = name
        self.parent : Node = None 
        
    def get_parent(self):
        return self.parent

    def set_parent(self, parent) -> None:
        self.parent = parent
        
class Edge:
    def __init__(self, id : int, lane : str, departure_time : str, arrival_time : str, start_lat : float, start_lon : float, end_lat : float, end_lon : float) -> None:
        self.id : int = id
        self.lane : str = lane
        self.start_lon : float = start_lon
        self.start_lat : float = start_lat
        self.end_lon : float = end_lon
        self.end_lat : float = end_lat
        self.departure_time : str = departure_time
        self.arrival_time : str = arrival_time
        # self.departure_time : datetime = datetime.strptime(departure_time, "%H:%M:%S")
        # self.arrival_time : datetime = datetime.strptime(arrival_time, "%H:%M:%S")

        
class Graph:
    def __init__(self) -> None:
        self.data = dict(dict(list()))
        
    def start_node_name_exists(self, node_name : str) -> bool:
        return node_name in self.data
    
    def end_node_name_exists(self, start_node_name : str, end_node_name : str) -> bool:
        return end_node_name in self.data[start_node_name]
        
    def add_start_node(self, node_name : str) -> None:
        self.data[node_name] = dict()

    def add_end_node(self, start_node_name : str, end_node_name : str) -> None:
        self.data[start_node_name][end_node_name] = list()

    def does_such_connection_exist(self, element, edge):
        if(element.lane == edge.lane and element.departure_time == edge.departure_time and element.arrival_time == edge.arrival_time):
            return True
        return False

    def is_former_earlier(self, time1 : str, time2 : str) -> bool:
        time1 = time1.split(":")
        time2 = time2.split(":")
        if (int(time1[0]) < int(time2[0])): return True
        elif ((int(time1[0]) == int(time2[0])) and (int(time1[1]) < int(time2[1]))): return True 
        return False
    
    def is_correct_node(self, node : Node, end : str) -> bool:
        return node.name == end

    def add_edge(self, start_node : str, end_node : str, edge : Edge):
        # adding in chronological order 
        i = 0
        was_added = False
        for element in self.data[start_node][end_node]:
            if(not self.does_such_connection_exist(element, edge)):
                if self.is_former_earlier(element.departure_time, edge.departure_time):
                    i += 1
                else:
                    self.data[start_node][end_node].insert(i, edge)
                    was_added = True
                    break
            else:
                i += 1
                was_added = True
                break
        if (not was_added):
            self.data[start_node][end_node].append(edge)

        
        # #adding normally
        # self.data[start_node][end_node].append(edge)

    def dijkstra(self, start_node_name, end_node_name, start_time, criterion='t'):
        visited = set()
        queue = dict()
        start = Node(start_node_name)
        current_node = start
        if (self.is_correct_node(current_node, end_node_name)): return "Start node is end node"
        for

        
def load_data_from_csv(filename):
    graph = Graph()
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        i = 0
        for row in reader:
            if(not graph.start_node_name_exists(row[5])):
                graph.add_start_node(row[5])
            if(not graph.end_node_name_exists(row[5], row[6])):
                graph.add_end_node(row[5], row[6])
            edge = Edge(row[0], row[2], row[3], row[4], row[7], row[8], row[9], row[10])
            graph.add_edge(row[5], row[6], edge)
            # if (i == 10000): break
            # if (i == 5822):
            #     pass
            # i += 1
    return graph   

start_time = time.time()
graph = load_data_from_csv(FILE_PATH)
for key1, inner_dict in graph.data.items():
    print(key1)
    for key2, inner_list in inner_dict.items():
        print("  ", key2)
        for item in inner_list:
            print("    ", item.lane, item.departure_time, item.arrival_time)
end_time = time.time()
execution_time = end_time - start_time
print("Czas: ", execution_time)


































# class Node:
#     def __init__(self, name : str, latitude : float, longitude : float) -> None:
#         self.name : str = name
#         self.latitude : float = latitude
#         self.longitude : float = longitude
#         self.children : dict = dict()
#         self.parent : Node = None
        
#     def add_child(self, child : Node) -> None:
#         self.children[child] = list()
        
#     def add_connection(self, child : Node, connection : Edge) -> None:
#         self.children[child].append(connection)
        
#     def get_parent(self) -> None:
#         return self.parent
    
#     def get_child(self, child : Node) -> None:
#         return self.children[child]
        
# class Edge:
#     def __init__(self, id : int, lane : str, departure_time : datetime, arrival_time : datetime) -> None:
#         self.id : int = id
#         self.lane : str = lane
#         self.departure_time : datetime = departure_time
#         self.arrival_time : datetime = arrival_time
        
# class Graph:
#     def __init__(self) -> None:
#         self.nodes = set(Node)
        
#     def node_name_exists(self, node_name : str, node_latitude : float, node_longitude : float) -> bool:
#         for node in self.nodes:
#             if (node.name == node_name and node.latitude == node_latitude and node.longitude == node_longitude): return True
#         return False
        
#     def add_node(self, node : Node) -> None:
#         self.nodes.update(node)
        
#     def add_edge(self, start_node : Node, end_node : Node, edge : Edge) -> None:
#         node : Node = self.nodes[start_node]
#         pass
        
#     def load_data_from_csv(filename):
#         graph = Graph()
#         with open(filename, 'r', encoding='utf-8') as file:
#             reader = csv.reader(file)
#             next(reader)  # Skip header row
#             for row in reader:
#                 if(not graph.node_name_exists(row['start_stop'], row['start_stop_lat'], row['start_stop_lon'])):
#                     pass
                
#                 start_node = Node(row['start_stop'], row['start_stop_lat'], row['start_stop_lon'])
#                 end_node = Node(row['end_stop'], row['end_stop_lat'], row['end_stop_lon'])
#                 edge = Edge(row['id'], row['lane'], datetime.strptime(row['departure_time'], "%H:%M:%S"), datetime.strptime(row['arrival_time'], "%H:%M:%S"))
                
#         return graph   