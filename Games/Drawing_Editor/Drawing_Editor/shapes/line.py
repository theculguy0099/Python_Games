from .shape import Shape

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color, width, obj_id=None, **kwargs):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        self.obj_id = obj_id
        self.kwargs = kwargs

    def draw(self, canvas):
        return canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color, width=self.width, **self.kwargs)

    def distance_from_point(self, x, y):
        # Using the formula for the distance between a point and a line
        # https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
        numerator = abs((self.y2 - self.y1) * x - (self.x2 - self.x1) * y + self.x2 * self.y1 - self.y2 * self.x1)
        denominator = ((self.y2 - self.y1) ** 2 + (self.x2 - self.x1) ** 2) ** 0.5
        return numerator / denominator
    def set_coords(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_coords(self):
        return self.x1, self.y1, self.x2, self.y2