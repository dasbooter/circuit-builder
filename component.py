class Component:
    def __init__(self, name, component_type):
        self.name = name
        self.component_type = component_type  # 'source', 'sink', or 'passive'
        self.connections = []

    def connect(self, other):
        if other not in self.connections:
            self.connections.append(other)
        if self not in other.connections:
            other.connections.append(self)
        print(f"Connected {self.name} to {other.name}")

    def is_connected_to(self, other, visited=None):
        if visited is None:
            visited = set()

        if self == other:
            return True

        visited.add(self)

        for connection in self.connections:
            if connection not in visited and connection.is_connected_to(other, visited):
                return True

        return False

    def print_connections(self):
        for connection in self.connections:
            print(f"{self.name} is connected to {connection.name}")
