from random import randrange

class Maze:
    location_opposite = (3, 2, 1, 0)
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.create_blank()
        self.create_dfs()

    def create_blank(self):
        return [[self.create_cell(x, y) for y in range(self.height)] for x in range(self.width)]
        
    def create_cell(self, x, y):
        return {'visited': 0, 'x': x, 'y': y, 'neighbors': [1, 1, 1, 1]}

    def create_dfs(self):
        self.create_maze(self.cells[0][0])
        # remove walls from maze entry ...
        self.remove_wall(self.cells[0][0], 0)
        # ... and exit
        self.remove_wall(self.cells[self.width - 1][self.height - 1], 3)
        
    def create_maze(self, cell):
        cell['visited'] = 1
        
        unvisited = self.get_unvisited_neighbors(cell)
        while len(unvisited) > 0:
            neighbor_index = unvisited.pop(randrange(len(unvisited)))
            neighbor = self.find_neighbor_by_location(cell, neighbor_index)
            
            if neighbor and not neighbor['visited']:
                self.remove_wall(cell, neighbor_index, neighbor)
                self.create_maze(neighbor)

    def get_unvisited_neighbors(self, cell):
        unvisited = []
        for i in range(len(cell['neighbors'])):
            if cell['neighbors'][i]:
                unvisited.append(i)
        return unvisited
        
    def find_neighbor_by_location(self, cell, location):
        col = cell['x']
        row = cell['y']
        if location == 0: # top
            row = row - 1
        elif location == 1: # left
            col = col - 1
        elif location == 2: # right
            col = col + 1
        else: # bottom
            row = row + 1
            
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return None
        
        return self.cells[col][row]
                
    def remove_wall(self, cell, neighbor_index, neighbor = None):
        cell['neighbors'][neighbor_index] = 0
        if neighbor:
            cell_index = self.location_opposite[neighbor_index]
            neighbor['neighbors'][cell_index] = 0
            
    def get_cell_walls(self, row, col):
        walls = []
        locations = self.cells[row][col]['neighbors']
        for location in range(len(locations)):
            if locations[location]:
                walls.append(location)
        return walls
        
if __name__ == '__main__':
    print "Maze"
