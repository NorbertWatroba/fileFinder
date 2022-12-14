import customtkinter
from PIL import Image
from functools import partial

from queries import get_all_categories, get_assigned_categories, assign_category, discharge_category, create_category


class Describe(customtkinter.CTk):
    def __init__(self, path: tuple):
        super().__init__()

        # defining window
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.minsize(180, 0)

        self.root = customtkinter.CTkFrame(self, fg_color='#101010', corner_radius=0)
        self.root.pack(expand=True, fill='both')

        # collecting data
        self.categories = get_all_categories()
        self.path = path
        self.assigned_cat = get_assigned_categories(self.path[0])

        # creating menu
        self.menu = customtkinter.CTkFrame(self.root, fg_color='#1c1c1c')
        self.category_creation, self.entry = self.create_category_creator()
        self.category_selection = self.create_category_selection()
        self.menu.pack(expand=True, fill='both', padx=5, pady=5)

    def create_category_selection(self):
        categories_frame = customtkinter.CTkFrame(self.menu, fg_color='transparent')
        categories_frame.grid_columnconfigure(0, weight=1)
        categories_frame.grid_columnconfigure(1, weight=1)

        index = 0
        for category in self.categories:
            checkbox = customtkinter.CTkCheckBox(categories_frame, text=category[1],
                                                 onvalue=f'+{category[0]}', offvalue=f'-{category[0]}',
                                                 border_width=1, width=0, height=20,
                                                 checkbox_width=20, checkbox_height=20,
                                                 command=partial(self.manage_categories, categories_frame),
                                                 border_color='#555555')
            if category[0] in self.assigned_cat:
                checkbox.select()
            checkbox.grid(column=index % 2, row=index // 2, pady=3, padx=10, sticky='w')
            index += 1
        categories_frame.pack(anchor='n', fill='x', pady=7, before=self.category_creation)
        return categories_frame

    def create_category_creator(self):
        new_category_frame = customtkinter.CTkFrame(self.menu, fg_color='transparent')
        entry = customtkinter.CTkEntry(new_category_frame, border_width=1, fg_color='transparent',
                                       placeholder_text='new category', border_color='#555555')
        entry.pack(pady=10)
        add = customtkinter.CTkButton(new_category_frame, text='add', width=65, height=25,
                                      command=self.adding_category)
        add.pack()
        new_category_frame.pack(fill='x', padx=10, pady=10)
        return new_category_frame, entry

    def manage_categories(self, frame: customtkinter.CTkFrame):
        action_list = []

        for child in frame.winfo_children():
            if isinstance(child, customtkinter.CTkCheckBox):
                action_list.append(child.get())

        for action in action_list:

            if action[0] == '+' and int(action[1:]) not in self.assigned_cat:
                assign_category(self.path[0], int(action[1:]))
                self.assigned_cat = get_assigned_categories(self.path[0])

            elif action[0] == '-' and int(action[1:]) in self.assigned_cat:
                discharge_category(self.path[0], int(action[1:]))
                self.assigned_cat = get_assigned_categories(self.path[0])

    def adding_category(self):

        create_category(self.entry.get())

        # update data
        self.categories = get_all_categories()
        self.assigned_cat = get_assigned_categories(self.path[0])

        # create new menu
        self.menu.pack_forget()
        self.menu = customtkinter.CTkFrame(self.root, fg_color='#1c1c1c')
        self.category_creation, self.entry = self.create_category_creator()
        self.category_selection = self.create_category_selection()
        self.menu.pack(expand=True, fill='both', padx=5, pady=5)

