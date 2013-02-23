class MazeDrawerPyro:
    border_color = "cadetblue"

    def __init__(self, sim, width = 0.0, height = 0.0, offset = 0.0):
        self.sim = sim
        self.width = width
        self.height = height
        self.offset = offset
    
    def initialize(self):
        self.width = self.width + 2.0 * self.offset
        self.height = self.height + 2.0 * self.offset
        self.draw_borders()

    def draw_line(self, x1, y1, x2, y2):
        self.sim.addWall(x1, y1, x2, y2)
        #self.sim.addBox(x1 - .05, y1 - .05, x2 + .05, y2 + .05, "black")

    def draw_borders(self):
        offset = self.offset / 2.0
        offset = -0.35
        self.sim.addBox(0.0 + offset, 0.0 + offset, self.width - offset, self.height - offset, self.border_color)
        offset = -0.25
        self.sim.addBox(0.0 + offset, 0.0 + offset, self.width - offset, self.height - offset)

    def finalize(self):
        pass
