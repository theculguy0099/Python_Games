from .shape import Shape

class Rectangle(Shape):
    def __init__(self, x1, y1, x2, y2, color, width, obj_id=None, rounded=False, **kwargs):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        self.obj_id = obj_id
        self.rounded = rounded
        self.kwargs = kwargs

    def draw_rounded_rect(self, x1, y1, x2, y2, width, color, canvas, radius=25, **kwargs):
        if x2 - x1 < 2 * radius:
            x2 = x1 + 2 *radius
        if y2 - y1 < 2 * radius:
            y2 = y1 + 2 *radius

        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]

        return canvas.create_polygon(points, outline=color, width=width, fill="",
                                        smooth=True, **kwargs)
    def draw(self, canvas):
        if self.rounded:
            return self.draw_rounded_rect(self.x1, self.y1, self.x2, self.y2, self.width, self.color, canvas, 25, **self.kwargs)
        else:
            return canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.color, width=self.width, **self.kwargs)

    def distance_from_point(self, x, y):
        if abs(x - self.x1) < 20 or abs(x - self.x2) < 20 or abs(y - self.y1) < 20 or abs(y - self.y2) < 20:
            return min([abs(x - self.x1), abs(x - self.x2), abs(y - self.y1), abs(y - self.y2)])
        return 100

    def set_coords(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_coords(self):
        return self.x1, self.y1, self.x2, self.y2
