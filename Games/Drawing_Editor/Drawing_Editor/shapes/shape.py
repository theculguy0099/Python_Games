from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self, canvas):
        pass

    def distance_from_point(self, x, y):
        pass

    def set_coords(self, x1, y1, x2, y2):
        pass

    def set_obj_id(self, obj_id):
        self.obj_id = obj_id

    def get_coords(self):
        pass