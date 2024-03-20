from Edge import Edge
class Node:
    def __init__(self, name : str, latitude : float, longitude : float) -> None:
        self.name : str = name
        self.latitude : float = latitude
        self.longitude : float = longitude

        # self.parent : Node = None
        # self.used_line : str = None
        self.latitude_list : list = [latitude]
        self.longitude_list : list = [longitude]
        self.connections : dict = dict()

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, Node) and self.name == other.name
    
    def __hash__(self):
        return hash((self.name))
    
    def to_string(self) -> str:
        return self.name
    
    #print connections to the given node
    def print_connections(self, end_node):
        for connection in self.connections[end_node]:
            print("\t\t", connection.line, " ", connection.departure_time, " ", connection.arrival_time)
    
    #adds end node to dict connections and returns list
    def work_on_end_node(self, node):
        already_exists = False
        for key, value in self.connections.items():
            if (key.name == node.name):
                already_exists = True
                break
                # return self.connections[node]
        if(not already_exists):
            self.connections.update({node : list()})
        # return self.connections[node]
    
    #adds edge to connection list
    def work_on_connection(self, end_node, id, line, departure_time, arrival_time):
        if(self.is_former_earlier(departure_time, arrival_time)):
            i = 0
            was_added = False
            # print("end_node =\t\t\t\t\t\t\t\t\t\t", end_node)
            # print("self.connections =\t\t\t\t\t\t", self.connections)
            edge_list = self.connections[end_node]
            # print("self.connections[end_node] =\t", edge_list)
            for element in edge_list:
                if(element.line == line and element.arrival_time == arrival_time and element.departure_time == departure_time):
                    was_added = True
                    break
                else:
                    if(self.is_former_earlier(element.departure_time, departure_time)):
                        i += 1
                    else:
                        edge = Edge(id, line, departure_time, arrival_time)
                        edge_list.insert(i, edge)
                        was_added = True
                        break
            if (not was_added):
                edge = Edge(id, line, departure_time, arrival_time)
                edge_list.append(edge)

    def is_former_earlier(self, time1 : str, time2 : str) -> bool:
        time1 = time1.split(":")
        time2 = time2.split(":")
        if (int(time1[0]) < int(time2[0])): return True
        elif ((int(time1[0]) == int(time2[0])) and (int(time1[1]) < int(time2[1]))): return True 
        return False

    def recalculate_coordinates(self, latitude : float, longitude : float) -> None:
        if (latitude not in self.latitude_list):
            self.latitude_list.append(latitude)
            latitude_help : float = 0
            size : int = len(self.latitude_list)
            for i in range(size):
                latitude_help += float(self.latitude_list[i])
            self.latitude = latitude_help / size

        if(longitude not in self.longitude_list):
            self.longitude_list.append(longitude)
            longitude_help : float = 0
            size : int = len(self.latitude_list)
            for i in range(size):
                longitude_help += float(self.longitude_list[i])
            self.longitude = longitude_help / size

    def calculate_time_difference(self, departure_time : str, desired_time : str):
        departure_time = departure_time.split(":")
        desired_time = desired_time.split(":")
        departure_time = int(departure_time[0]) * 3600 + int(departure_time[1]) * 60 + int(departure_time[2])
        desired_time = int(desired_time[0]) * 3600 + int(desired_time[1]) * 60 + int(desired_time[2])
        return departure_time - desired_time

    def get_quickest_connection_to_node(self, end_node_name, desired_time):
        best_time_difference = 86400
        best_connection = None
        for element in self.connections[end_node_name]:
            time_difference = self.calculate_time_difference(element.departure_time, desired_time)
            if(time_difference < 0): break
            if(time_difference < best_time_difference):
                best_time_difference = time_difference
                best_connection = element
        return best_connection