from tkinter import messagebox
class Save:

    @staticmethod
    def write_group(group, canvas, file):
        file.write("begin\n")
        for obj in canvas.group_manager.group_adj_list[group]:
            if isinstance(obj, int):
                canvas_obj = canvas.find_withtag(obj)[0]
                obj_type = canvas.type(canvas_obj)
                if obj_type == "line":
                    coords = canvas.coords(canvas_obj)
                    coords = list(map(int, coords))
                    color = canvas.itemcget(canvas_obj, "fill")
                    color_code = canvas.color_manager.get_color_code(color)
                    line_str = f"line {' '.join(map(str, coords))} {color_code}"
                    file.write(line_str + "\n")
                elif obj_type == "rectangle":
                    coords = None
                    if canvas.Obj_Dict[canvas_obj].rounded:
                        coords = canvas.Obj_Dict[canvas_obj].get_coords()
                    else:
                        coords = canvas.coords(canvas_obj)

                    coords = list(map(int, coords))
                    color = canvas.itemcget(canvas_obj, "outline")
                    color_code = canvas.color_manager.get_color_code(color)
                    style = "r" if canvas.gettags(canvas_obj) == ("rounded_rectangle",) else "s"
                    rect_str = f"rect {' '.join(map(str, coords))} {color_code} {style}"
                    file.write(rect_str + "\n")
            else:
                Save.write_group(obj, canvas, file)
        file.write("end\n")

    @staticmethod
    def save(file, canvas):
        for line in canvas.Lines:
            if canvas.group_manager.find_group(line):
                continue
            coords = canvas.coords(line)
            coords = list(map(int, coords))
            color = canvas.itemcget(line, "fill")
            color_code = canvas.color_manager.get_color_code(color)
            line_str = f"line {' '.join(map(str, coords))} {color_code}"
            file.write(line_str + "\n")

        for rectangle in canvas.Rectangles:
            if canvas.group_manager.find_group(rectangle):
                continue
            coords = None
            if canvas.Obj_Dict[rectangle].rounded:
                coords = canvas.Obj_Dict[rectangle].get_coords()
            else:
                coords = canvas.coords(rectangle)
            coords = list(map(int, coords))
            color = canvas.itemcget(rectangle, "outline")
            color_code = canvas.color_manager.get_color_code(color)
            rect_class = canvas.Obj_Dict[rectangle]
            style = "s"
            rounded = rect_class.rounded
            if rounded:
                style = "r"
            rectangle_str = f"rectangle {' '.join(map(str, coords))} {color_code} {style}"
            file.write(rectangle_str + "\n")

        for groups in canvas.group_manager.root_groups:
            Save.write_group(groups, canvas, file)

class Open:

    def openFile(file,canvas):
        if canvas.has_unsaved_changes():
            response = messagebox.askyesnocancel("Save changes", "Do you want to save changes before opening a new file?")
            if response is None:
                return
            elif response:
                canvas.save_file()

        canvas.unselect_all()
        canvas.Lines = []
        canvas.Rectangles = []
        canvas.group_manager.clear_all()

        for line in file:
            line = line.strip()
            if line.startswith("line"):
                _, x1, y1, x2, y2, color = line.split()
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                color = canvas.color_manager.get_color_name(color)
                canvas.draw("line", color, canvas.buttons.size_button.get(), [x1, y1, x2, y2])
            elif line.startswith("rect"):
                _, x1, y1, x2, y2, color, style = line.split()
                x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                color = canvas.color_manager.get_color_name(color)
                canvas.draw("rounded_rectangle" if style == "r" else "rectangle", color, canvas.buttons.size_button.get(), [x1, y1, x2, y2])
            elif line == "begin":
                canvas.group_manager.group_counter += 1
                group_name = f"group{canvas.group_manager.group_counter}"
                canvas.group_manager.group_adj_list[group_name] = []
                Open.load_group_from_file(file, canvas, group_name)
                canvas.group_manager.root_groups.append(group_name)
            elif line == "end":
                continue

    def load_group_from_file(file, canvas, group_name):
        current_group = group_name
        for line in file:
            line = line.strip()
            if line.startswith("begin"):
                canvas.group_manager.group_counter += 1
                group_name_f = f"group{canvas.group_manager.group_counter}"
                canvas.group_manager.group_adj_list[group_name_f] = []
                generated_group = Open.load_group_from_file(file, canvas, group_name_f)
                canvas.group_manager.group_adj_list[current_group].append(generated_group)
            elif line.startswith("end"):
                return current_group
            else:
                if line.startswith("line"):
                    _, x1, y1, x2, y2, color = line.split()
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    color = canvas.color_manager.get_color_name(color)
                    obj = canvas.draw("line", color, canvas.buttons.size_button.get(), [x1, y1, x2, y2])
                    if current_group is not None:
                        canvas.group_manager.group_adj_list[current_group].append(obj)
                elif line.startswith("rect"):
                    _, x1, y1, x2, y2, color, style = line.split()
                    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
                    color = canvas.color_manager.get_color_name(color)
                    obj = canvas.draw("rounded_rectangle" if style == "r" else "rectangle", color, canvas.buttons.size_button.get(), [x1, y1, x2, y2])
                    # obj_coords = canvas.coords(obj)
                    obj_coords = None
                    if canvas.Obj_Dict[obj].rounded:
                        obj_coords = canvas.Obj_Dict[obj].get_coords()
                    else:
                        obj_coords = canvas.coords(obj)
                    if current_group is not None:
                        canvas.group_manager.group_adj_list[current_group].append(obj)
        return current_group


