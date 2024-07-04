from .line import Line
from .rectangle import Rectangle

class ShapesManager(Line, Rectangle):
    def __init__(self):
        self.selected_object = []
        self.initial_move_coords = None
        self.bounding_box = {}

    def move_objects(self, dx, dy, canvas):
        if not self.selected_object:
            return
        if self.initial_move_coords:
            for i, obj in enumerate(self.selected_object):
                if not self.initial_move_coords[i]:
                    continue
                x1, y1, x2, y2 = self.initial_move_coords[i]
                canvas.move(obj, dx, dy)
                canvas.move(self.bounding_box[obj], dx, dy)
                canvas.Obj_Dict[obj].set_coords(x1 + dx, y1 + dy, x2 + dx, y2 + dy)
                self.initial_move_coords[i] = [x1 + dx, y1 + dy, x2 + dx, y2 + dy]

    def delete_objects(self, canvas):
        for obj in self.selected_object:
            canvas.delete(obj)
            canvas.delete(self.bounding_box[obj])
            canvas.Obj_Dict.pop(obj)
            if obj in canvas.Lines:
                canvas.Lines.remove(obj)
            elif obj in canvas.Rectangles:
                canvas.Rectangles.remove(obj)
        self.selected_object = []
        self.initial_move_coords = None

    def select_object(self, obj):
        self.selected_object.append(obj)

    def deselect_object(self, obj):
        self.selected_object.remove(obj)

    def is_selected(self, obj):
        return obj in self.selected_object

    def draw_bounding_box(self, canvas, obj, padding=5):
        # obj_coords = canvas.coords(obj)
        obj_coords = None
        if obj in canvas.Obj_Dict:
            if canvas.Obj_Dict[obj].rounded:
                obj_coords = canvas.Obj_Dict[obj].get_coords()
            else:
                obj_coords = canvas.coords(obj)
        if not obj_coords:
            return
        x1, y1, x2, y2 = obj_coords
        bbox_x1 = x1 - padding
        bbox_y1 = y1 - padding
        bbox_x2 = x2 + padding
        bbox_y2 = y2 + padding
        bbox = canvas.create_rectangle(bbox_x1, bbox_y1, bbox_x2, bbox_y2, outline="red", dash=(4, 4), tags="bounding_box")
        self.bounding_box[obj] = bbox

    def update_selected_objects(self, canvas, unselect=False):
        canvas.delete("bounding_box")
        if not unselect:
            for obj in self.selected_object:
                self.draw_bounding_box(canvas, obj)
        canvas.update()

    def unselect_all(self, canvas):
        self.update_selected_objects(canvas, unselect=True)
        self.selected_object = []
        self.initial_move_coords = None