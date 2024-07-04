import xml.etree.ElementTree as ET

class ExportManager:

    def export_to_xml(self, file_path, canvas):

        self.xml_root = ET.Element("drawing")

        for line in canvas.Lines:
            if canvas.group_manager.find_group(line):
                continue
            line_elem = ET.Element("line")
            self.xml_root.append(line_elem)

            begin_elem = ET.Element("begin")
            line_elem.append(begin_elem)

            x1, y1, x2, y2 = canvas.coords(line)
            ET.SubElement(begin_elem, "x").text = str(int(x1))
            ET.SubElement(begin_elem, "y").text = str(int(y1))

            end_elem = ET.Element("end")
            line_elem.append(end_elem)
            ET.SubElement(end_elem, "x").text = str(int(x2))
            ET.SubElement(end_elem, "y").text = str(int(y2))

            color = canvas.itemcget(line, "fill")
            ET.SubElement(line_elem, "color").text = color

        for rect in canvas.Rectangles:
            if canvas.group_manager.find_group(rect):
                continue
            rect_elem = ET.Element("rectangle")
            self.xml_root.append(rect_elem)

            x1, y1, x2, y2 = None, None, None, None
            if canvas.Obj_Dict[rect].rounded:
                x1, y1, x2, y2 = canvas.Obj_Dict[rect].get_coords()
            else:
                x1, y1, x2, y2 = canvas.coords(rect)

            upper_left_elem = ET.Element("upper-left")
            rect_elem.append(upper_left_elem)
            ET.SubElement(upper_left_elem, "x").text = str(int(x1))
            ET.SubElement(upper_left_elem, "y").text = str(int(y1))

            lower_right_elem = ET.Element("lower-right")
            rect_elem.append(lower_right_elem)
            ET.SubElement(lower_right_elem, "x").text = str(int(x2))
            ET.SubElement(lower_right_elem, "y").text = str(int(y2))

            color = canvas.itemcget(rect, "outline")
            ET.SubElement(rect_elem, "color").text = color

            corner = "rounded" if canvas.gettags(rect) == ("rounded_rectangle",) else "square"
            ET.SubElement(rect_elem, "corner").text = corner

        for group_name in canvas.group_manager.root_groups:
            self.export_group_to_xml(self.xml_root, group_name, canvas)

        tree = ET.ElementTree(self.xml_root)
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)

    def export_group_to_xml(self, parent, group_name, canvas):
        group_elem = ET.Element("group")
        parent.append(group_elem)

        for obj in canvas.group_manager.group_adj_list[group_name]:
            if isinstance(obj, int):
                canvas_obj = canvas.find_withtag(obj)[0]
                obj_type = canvas.type(canvas_obj)
                if obj_type == "line":
                    line_elem = ET.Element("line")
                    group_elem.append(line_elem)

                    x1, y1, x2, y2 = canvas.coords(canvas_obj)
                    begin_elem = ET.Element("begin")
                    line_elem.append(begin_elem)
                    ET.SubElement(begin_elem, "x").text = str(int(x1))
                    ET.SubElement(begin_elem, "y").text = str(int(y1))

                    end_elem = ET.Element("end")
                    line_elem.append(end_elem)
                    ET.SubElement(end_elem, "x").text = str(int(x2))
                    ET.SubElement(end_elem, "y").text = str(int(y2))

                    color = canvas.itemcget(canvas_obj, "fill")
                    ET.SubElement(line_elem, "color").text = color

                elif obj_type == "rectangle":
                    rect_elem = ET.Element("rectangle")
                    group_elem.append(rect_elem)

                    # x1, y1, x2, y2 = canvas.coords(canvas_obj)
                    x1, y1, x2, y2 = None, None, None, None
                    if canvas.Obj_Dict[canvas_obj].rounded:
                        x1, y1, x2, y2 = canvas.Obj_Dict[canvas_obj].get_coords()
                    else:
                        x1, y1, x2, y2 = canvas.coords(canvas_obj)

                    upper_left_elem = ET.Element("upper-left")
                    rect_elem.append(upper_left_elem)
                    ET.SubElement(upper_left_elem, "x").text = str(int(x1))
                    ET.SubElement(upper_left_elem, "y").text = str(int(y1))

                    lower_right_elem = ET.Element("lower-right")
                    rect_elem.append(lower_right_elem)
                    ET.SubElement(lower_right_elem, "x").text = str(int(x2))
                    ET.SubElement(lower_right_elem, "y").text = str(int(y2))

                    color = canvas.itemcget(canvas_obj, "outline")
                    ET.SubElement(rect_elem, "color").text = color

                    corner = "rounded" if canvas.gettags(canvas_obj) == ("rounded_rectangle",) else "square"
                    ET.SubElement(rect_elem, "corner").text = corner

            else:
                self.export_group_to_xml(group_elem, obj, canvas)

