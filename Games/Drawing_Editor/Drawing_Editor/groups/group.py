class Group:
    def __init__(self):
        self.group_adj_list = {}
        self.root_groups = []
        self.group_counter = 0
        self.current_selected_list = []

    def is_object_in_group(self, obj, parent_group):
        for element in self.group_adj_list[parent_group]:
            if type(element) == int:
                if element == obj:
                    return True
            else:
                if self.is_object_in_group(obj, element):
                    return True
        return False

    def find_group(self, obj):
        for group in self.root_groups:
            if self.is_object_in_group(obj, group):
                return group
        return None

    def get_elements(self, group):
        elements = []
        for element in self.group_adj_list[group]:
            if type(element) == int:
                elements.append(element)
            else:
                elements += self.get_elements(element)
        return elements

    def add_to_current_selected_list(self, obj):
        self.current_selected_list.append(obj)
    
    def clear_current_selected_list(self):
        self.current_selected_list = []

    def add_selected_objects(self):
        if len(self.current_selected_list) <= 1:
            return
        if self.root_groups == []:
            self.group_counter += 1
            group_name = "group " + str(self.group_counter)
            self.group_adj_list[group_name] = self.current_selected_list
            self.root_groups.append(group_name)
        else:
            num = ""
            ct = 0
            for obj in self.current_selected_list:
                if type(obj) == int:
                    ct += 1
                else:
                    num += obj[5:]
                    self.root_groups.remove(obj)
            if num != "":
                if ct > 0:
                    self.group_counter += 1
                    num += str(self.group_counter)
                self.group_adj_list["group " + num] = self.current_selected_list
                self.root_groups.append("group " + num)
            else:
                self.group_counter += 1
                group_name = "group " + str(self.group_counter)
                self.group_adj_list[group_name] = self.current_selected_list
                self.root_groups.append(group_name)

    def ungroup_one_level(self):
        if len(self.current_selected_list) != 1:
            return
        group = self.current_selected_list[0]
        if type(group) != str:
            return
        self.root_groups.remove(group)
        for obj in self.group_adj_list[group]:
            if type(obj) == str:
                self.root_groups.append(obj)
        self.group_adj_list.pop(group)
        print("root groups: ", self.root_groups)
        print("group adj list: ", self.group_adj_list)

    def ungroup_recursive(self, group):
        for obj in self.group_adj_list[group]:
            if type(obj) == str:
                self.ungroup_recursive(obj)
        self.group_adj_list.pop(group)

    def ungroup_all_selected(self):
        if len(self.current_selected_list) == 0:
            return
        if len(self.current_selected_list) > 1:
            return
        group = self.current_selected_list[0]
        if type(group) != str:
            return
        self.root_groups.remove(group)
        self.ungroup_recursive(group)
        print("root groups: ", self.root_groups)
        print("group adj list: ", self.group_adj_list)

    def clear_all(self):
        self.group_adj_list = {}
        self.root_groups = []
        self.group_counter = 0
        self.current_selected_list = []