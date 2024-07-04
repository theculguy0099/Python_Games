from tkinter import Canvas
from tkinter import *
from shapes import Rectangle, Line
from shapes import ShapesManager
from colors import Color, ColorManager
from groups import Group
from inputoutput import ClipBoardManager, Save, Open, ExportManager
from .buttons import Buttons
from .dialogs import SaveFileDialog, OpenFileDialog, ExportDialog, CustomDialog
import copy

class Canvas(Canvas):
    def __init__(self, root):
        super().__init__(root, width=400, height=400, background="white")
        self.pack(fill="both")
        self.pack(side="right", fill="both", expand=True)
        self.bind("<Motion>", self.on_motion)
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.Lines = []
        self.Rectangles = []
        self.Obj_Dict = {}
        self.unsaved_changes = False
        self.selection_range = 20


        self.button_frame = Frame(root)
        self.button_frame.pack(side="left", fill="y")
        self.buttons = Buttons(root, self)

        self.mouse_clicked = False
        self.drawing_tool = "arrow"
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None
        self.x_pos = None
        self.y_pos = None
        self.shapes_manager = ShapesManager()
        self.color_manager = ColorManager(root)
        self.group_manager = Group()
        self.copy_manager = ClipBoardManager()
        self.export_manager = ExportManager()

        menubar = Menu(root)
        filemenu = Menu(menubar)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)

        export_menu = Menu(filemenu)
        export_menu.add_command(label="Export to XML", command=lambda: self.export_xml())

        filemenu.add_cascade(label="Export", menu=export_menu)

        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)
        self.root = root

    def open_file(self):
        file_path = OpenFileDialog().show()
        if file_path:
            with open(file_path, "r") as file:
                Open.openFile(file, self)

    def save_file(self):
        file_path = SaveFileDialog().show()
        if file_path:
            with open(file_path, "w") as file:
                Save.save(file, self)

    def export_xml(self):
        file_path = ExportDialog().show(default_extension=".xml", file_types=[("XML files", "*.xml")])
        if file_path:
            self.export_manager.export_to_xml(file_path, self)

    def get_instance_list(self, obj_id):
        if obj_id in self.Lines:
            return self.Lines
        elif obj_id in self.Rectangles:
            return self.Rectangles

    def find_instance_from_id(self, obj_id):
        obj = self.Obj_Dict.get(obj_id)
        if obj:
            return obj
        return None

    def on_click(self, event):
        self.mouse_clicked = True
        self.x1 = event.x
        self.y1 = event.y

        if self.drawing_tool == "arrow":
            closest = self.find_closest(event.x, event.y)[0]
            if closest:
                distance = 0
                obj = self.find_instance_from_id(closest)
                print(obj)
                if obj:
                    distance = obj.distance_from_point(event.x, event.y)

                if distance <= self.selection_range:
                    if event.state & 0x0004: # Ctrl key
                        if self.shapes_manager.is_selected(closest):
                            self.shapes_manager.deselect_object(closest)
                        else:
                            group_name = self.group_manager.find_group(closest)
                            if group_name:
                                objects = self.group_manager.get_elements(group_name)
                                for obj in objects:
                                    self.shapes_manager.select_object(obj)
                                self.group_manager.add_to_current_selected_list(group_name)
                            else:
                                self.shapes_manager.select_object(closest)
                                self.group_manager.add_to_current_selected_list(closest)
                    else:
                        if not self.shapes_manager.is_selected(closest):
                            self.unselect_all()
                            group_name = self.group_manager.find_group(closest)
                            if group_name:
                                objects = self.group_manager.get_elements(group_name)
                                for obj in objects:
                                    self.shapes_manager.select_object(obj)
                                self.group_manager.add_to_current_selected_list(group_name)
                            else:
                                self.shapes_manager.select_object(closest)
                                self.group_manager.add_to_current_selected_list(closest)
                else:
                    self.unselect_all()
        self.shapes_manager.update_selected_objects(self)

        if self.shapes_manager.selected_object:
            # self.shapes_manager.initial_move_coords = [
            #     self.coords(obj) for obj in self.shapes_manager.selected_object
            # ]
            self.shapes_manager.initial_move_coords = []
            for obj in self.shapes_manager.selected_object:
                if obj in self.Lines:
                    self.shapes_manager.initial_move_coords.append(self.coords(obj))
                elif obj in self.Rectangles:
                    obj_coords = None
                    if self.Obj_Dict[obj].rounded:
                        obj_coords = self.Obj_Dict[obj].get_coords()
                    else:
                        obj_coords = self.coords(obj)
                    self.shapes_manager.initial_move_coords.append(obj_coords)

    def draw(self, tool, color, w, coordinates=[]):
        x_obj_id = None
        print(tool)
        if tool == "line":
            x = Line(coordinates[0], coordinates[1], coordinates[2], coordinates[3], color, w)
            obj_id = x.draw(self)
            x.set_obj_id(obj_id)
            x_obj_id = obj_id
            self.Obj_Dict[obj_id] = x
            self.Lines.append(obj_id)
        elif tool == "rectangle":
            x = Rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3], color, w)
            obj_id = x.draw(self)
            x.set_obj_id(obj_id)
            x_obj_id = obj_id
            self.Obj_Dict[obj_id] = x
            self.Rectangles.append(obj_id)
        elif tool == "rounded_rectangle":
            x = Rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3],
                          color, w, rounded=True)
            obj_id = x.draw(self)
            x.set_obj_id(obj_id)
            x_obj_id = obj_id
            self.Obj_Dict[obj_id] = x
            self.Rectangles.append(obj_id)
        return x_obj_id

    def on_release(self, event):
        self.delete("temp_objects")
        self.mouse_clicked = False

        if self.x_pos and self.y_pos and self.drawing_tool != "arrow":
            self.draw(self.drawing_tool, self.color_manager.color,
                      self.buttons.size_button.get(),
                      [self.x1, self.y1, self.x_pos, self.y_pos])

        self.x_pos = None
        self.y_pos = None
        self.shapes_manager.initial_move_coords = None

        self.x2 = event.x
        self.y2 = event.y

    def on_motion(self, event):
        self.delete("temp_objects")
        if self.mouse_clicked:
            if self.x_pos is not None and self.y_pos is not None:
                if self.drawing_tool == "line":
                    x = Line(self.x1, self.y1, self.x_pos, self.y_pos,
                             self.color_manager.color, self.buttons.size_button.get(),
                             tags="temp_objects")
                    x.draw(self)
                elif self.drawing_tool == "rectangle":
                    x = Rectangle(self.x1, self.y1, self.x_pos, self.y_pos,
                                  self.color_manager.color, self.buttons.size_button.get(),
                                  tags="temp_objects")
                    x.draw(self)
                elif self.drawing_tool == "rounded_rectangle":
                    x = Rectangle(self.x1, self.y1, self.x_pos, self.y_pos,
                                  self.color_manager.color, self.buttons.size_button.get(),
                                  rounded=True, tags="temp_objects")
                    x.draw(self)
                elif self.drawing_tool == "arrow":
                    dx = event.x - self.x_pos
                    dy = event.y - self.y_pos
                    self.shapes_manager.move_objects(dx, dy, self)
                    self.x2 = event.x
                    self.y2 = event.y
            self.x_pos = event.x
            self.y_pos = event.y
            self.unsaved_changes = True

    def delete_object(self):
        self.shapes_manager.delete_objects(self)

    def set_brush_type(self, brush_type):
        self.drawing_tool = brush_type

    def group_objects(self):
        self.group_manager.add_selected_objects()
        self.unselect_all()
        self.shapes_manager.update_selected_objects(self)

    def ungroup_objects(self):
        self.group_manager.ungroup_one_level()
        self.unselect_all()
        self.shapes_manager.update_selected_objects(self)

    def ungroup_all(self):
        self.group_manager.ungroup_all_selected()
        self.unselect_all()
        self.shapes_manager.update_selected_objects(self)

    def unselect_all(self):
        self.shapes_manager.unselect_all(self)
        self.group_manager.clear_current_selected_list()

    def copy_objects(self):
        current_selected_list = self.group_manager.current_selected_list
        if len(current_selected_list) == 0:
            return
        copied_objects = []
        for obj in current_selected_list:
            if type(obj) == int:
                obj = self.Obj_Dict[obj]
                if obj:
                    copied_objects.append(obj)
            else:
                copied_objects.append(self.recursive_copy(obj))
        self.copy_manager.copy(copied_objects)
        for obj in copied_objects:
            print(obj)

    def recursive_copy(self, group):
        copied_group = []
        for obj in self.group_manager.group_adj_list[group]:
            if type(obj) == int:
                obj = self.Obj_Dict[obj]
                if obj:
                    copied_group.append(obj)
            else:
                copied_group.append(self.recursive_copy(obj))
        return copied_group

    def paste_objects(self):
        if self.copy_manager.is_clipboard_empty():
            return
        copied_objects = self.copy_manager.paste()
        for obj in copied_objects:
            if type(obj) != list:
                offset = 10
                coords = obj.get_coords()
                new_coords = [coord + offset for coord in coords]
                x1, y1, x2, y2 = new_coords
                obj_copy = copy.deepcopy(obj)
                obj_copy.set_coords(x1, y1, x2, y2)
                obj_id = obj_copy.draw(self)
                obj_copy.set_obj_id(obj_id)
                self.Obj_Dict[obj_id] = obj_copy
                if type(obj) == Line:
                    self.Lines.append(obj_id)
                else:
                    self.Rectangles.append(obj_id)
            else:
                self.group_manager.group_counter += 1
                group_name = "group " + str(self.group_manager.group_counter)
                self.group_manager.group_adj_list[group_name] = []
                self.group_manager.root_groups.append(group_name)
                self.paste_recursive(obj, group_name)

    def paste_recursive(self, group, group_name):
        for obj in group:
            if type(obj) != list:
                offset = 10
                coords = obj.get_coords()
                new_coords = [coord + offset for coord in coords]
                x1, y1, x2, y2 = new_coords
                obj_copy = copy.deepcopy(obj)
                obj_copy.set_coords(x1, y1, x2, y2)
                obj_id = obj_copy.draw(self)
                obj_copy.set_obj_id(obj_id)
                self.Obj_Dict[obj_id] = obj_copy
                if type(obj) == Line:
                    self.Lines.append(obj_id)
                else:
                    self.Rectangles.append(obj_id)
                self.group_manager.group_adj_list[group_name].append(obj_id)
            else:
                self.group_manager.group_counter += 1
                new_group_name = "group " + str(self.group_manager.group_counter)
                self.group_manager.group_adj_list[new_group_name] = []
                self.group_manager.group_adj_list[group_name].append(new_group_name)
                self.paste_recursive(obj, new_group_name)

    def has_unsaved_changes(self):
        return self.unsaved_changes


    def edit_selected_object(self):
        if not self.shapes_manager.selected_object:
            return
        if len(self.shapes_manager.selected_object) > 1:
            print("Only one object can be edited at a time.")
            return

        obj = self.shapes_manager.selected_object[0]
        if obj in self.Lines:
            # For lines, allow editing color
            color_options = self.color_manager.get_color_options()
            color_dialog = CustomDialog(self.root,"line")
            # color_dialog.title("Edit Line")
            # color_dialog.label("Enter line color:")
            color = color_dialog.line_color
            coords = self.coords(obj)
            if color in color_options:
                self.delete_object()
                self.draw("line", color, self.buttons.size_button.get(), coords)
        elif obj in self.Rectangles:
            # For rectangles, allow editing line color and corner style
            dialog = CustomDialog(self.root, "rectangle")
            line_color = dialog.line_color
            corner_style = dialog.corner_style
            colors = self.color_manager.get_color_options()
            # coords = self.coords(obj)
            coords = None
            if self.Obj_Dict[obj].rounded:
                coords = self.Obj_Dict[obj].get_coords()
            else:
                coords = self.coords(obj)
            if line_color in colors and corner_style in [
                "square",
                "rounded",
            ]:
                # self.canvas.itemconfig(obj, outline=line_color)
                # # Apply corner style if applicable
                # if corner_style == "rounded":
                #     self.canvas.itemconfig(obj, dash=(5, 5))
                # else:
                #     self.canvas.itemconfig(obj, dash=())
                self.delete_object()
                if corner_style == "rounded":
                    self.draw("rounded_rectangle", line_color, self.buttons.size_button.get(), coords)
                else:
                    self.draw("rectangle", line_color, self.buttons.size_button.get(), coords)

