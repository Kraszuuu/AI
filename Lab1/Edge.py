class Edge:
    def __init__(self, id : int, line : str, departure_time : str, arrival_time : str) -> None:
        self.id : int = id
        self.line : str = line
        self.departure_time : str = departure_time
        self.arrival_time : str = arrival_time