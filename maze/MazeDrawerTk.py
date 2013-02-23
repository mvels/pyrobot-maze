from Tkinter import *

class MazeDrawerTk:
    def __init__(self, width = 0, height = 0, offset = 3):
        self.width = width
        self.height = height
        self.offset = offset
    
    def initialize(self):    
        self.width = self.width + 2 * self.offset
        self.height = self.height + 2 * self.offset
        
        self.master = Tk()
        self.w = Canvas(self.master, width = self.width, height = self.height)
        self.w.pack()
        # self.draw_borders()

    def draw_line(self, x1, y1, x2, y2):
        self.w.create_line(x1, y1, x2, y2)

    def draw_borders(self):
        offset = self.offset / 2
        self.w.create_rectangle(0 + offset, 0 + offset, self.width - offset, self.height - offset)
        # self.w.create_line(0 + offset, 0 + offset, self.width - offset, 0 + offset)
        # self.w.create_line(0 + offset, 0 + offset, 0 + offset, self.height - offset)
        # self.w.create_line(self.width - offset, 0 + offset, self.width - offset, self.height - offset)
        # self.w.create_line(0 + offset, self.height - offset, self.width - offset, self.height - offset)
    
    def finalize(self):
        self.master.mainloop()
