class MazeDrawer:
    offset = 0.0
    def __init__(self, width, height, offset = 0):
        self.width = width
        self.height = height
        self.offset = offset if offset else self.offset
        
    def init_drawer(self, drawer):
        drawer.width = self.width
        drawer.height = self.height
        drawer.offset = self.offset
        drawer.initialize()
        self.drawer = drawer

    def draw(self, maze, drawer):
        rows = maze.width
        cols = maze.height
        self.row_size = self.width / rows
        self.col_size = self.height / cols
        self.half_row = self.row_size / 2.0
        self.half_col = self.col_size / 2.0

        self.init_drawer(drawer)
        
        for row in range(rows):
            for col in range(cols):
                for location in maze.get_cell_walls(row, col):
                    self.draw_wall(row + 1.0, col + 1.0, location)
        
        self.drawer.finalize()
        
    def draw_wall(self, x, y, location):
        if location == 0: # top / north
            x1 = self.row_size * x - self.half_row
            x2 = self.row_size * x + self.half_row
            y1 = self.col_size * y - self.half_col
            y2 = y1
        elif location == 1: # left / west
            x1 = self.row_size * x - self.half_row
            x2 = x1
            y1 = self.col_size * y - self.half_col
            y2 = self.col_size * y + self.half_col
        elif location == 2: # right / east
            x1 = self.row_size * x + self.half_row
            x2 = x1
            y1 = self.col_size * y - self.half_col
            y2 = self.col_size * y + self.half_col
        elif location == 3: # bottom / south
            x1 = self.row_size * x - self.half_row
            x2 = self.row_size * x + self.half_row
            y1 = self.col_size * y + self.half_col
            y2 = y1
            
        offset_x = self.half_row * -1.0 + self.offset
        offset_y = self.half_col * -1.0 + self.offset
        self.drawer.draw_line(x1 + offset_x, y1 + offset_y, x2 + offset_x, y2 + offset_y)

if __name__ == '__main__':
    print "MazeDrawer"
