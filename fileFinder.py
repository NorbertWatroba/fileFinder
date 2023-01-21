import customtkinter
from PIL import Image

from functools import partial
from math import ceil

from utils import read_config
from queries import get_all_paths, get_all_categories, create_new_view
from describer import Describe


class FileFinder(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # defining window
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("fileFinder")
        self.geometry("700x450")
        self.root = customtkinter.CTkFrame(self, fg_color='#101010', corner_radius=0)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)
        self.root.pack(expand=True, fill='both')

        # collecting & defining data
        self.paths = get_all_paths()
        self.page_num = int(read_config().get('BOOKMARKS', 'RECENT'))
        self.total_pages = ceil(len(self.paths) / 6)
        self.settings_displayed = False

        self.settings_menu = self.create_settings_menu()

        # building home page
        self.footer = self.create_footer()
        self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

        self.page = self.create_page((700, 450))
        self.page.grid(column=0, row=0, sticky='nsew')

        # binds definition
        self.bind('<KeyPress-F5>', lambda e: self.resizer())
        self.bind('<KeyPress-Right>', lambda e: self.next_page())
        self.bind('<KeyPress-Left>', lambda e: self.previous_page())

        self.protocol('WM_DELETE_WINDOW', self.close)

    def create_footer(self):
        footer = customtkinter.CTkFrame(self.root, corner_radius=5, fg_color='#1c1c1c')
        footer.columnconfigure(0, weight=0)
        footer.columnconfigure(1, weight=1)
        footer.columnconfigure(2, weight=0)
        footer.columnconfigure(3, weight=1)
        footer.columnconfigure(4, weight=0)
        text = customtkinter.CTkLabel(footer,
                                      text=f'   {self.page_num + 1} / {self.total_pages}   ', height=65)
        text.grid(column=2, row=0)
        settings_btn = customtkinter.CTkButton(footer, text='X', command=self.settings, width=40, height=40)
        settings_btn.grid(column=0, row=0, padx=12.5)
        btn_f = customtkinter.CTkButton(footer, text='>', command=self.next_page, width=20, height=20)
        btn_f.grid(column=3, row=0, sticky='w')
        btn_p = customtkinter.CTkButton(footer, text='<', command=self.previous_page, width=20, height=20)
        btn_p.grid(column=1, row=0, sticky='e')
        placeholder = customtkinter.CTkFrame(footer, width=65, height=0)
        placeholder.grid(column=4, row=0)
        return footer

    def settings(self):
        self.settings_displayed = not self.settings_displayed
        if self.settings_displayed:
            # display window with settings menu
            self.root.columnconfigure(0, weight=0)
            self.root.columnconfigure(1, weight=1)
            self.root.rowconfigure(0, weight=1)
            self.root.rowconfigure(1, weight=0)
            self.root.pack(expand=True, fill='both')

            self.settings_menu = self.create_settings_menu()
            self.settings_menu.grid(column=0, row=0, sticky='nsew', padx=10, pady=5, ipady=50)

            self.footer.grid(column=0, columnspan=2, row=1, sticky='nsew', padx=10, pady=5)

            self.page = self.create_page((self.winfo_width() - self.settings_menu.winfo_width(), self.winfo_height()))
            self.page.grid(column=1, row=0, sticky='nsew')
        else:
            self.settings_menu.grid_forget()
            self.root.destroy()
            self.root = customtkinter.CTkFrame(self, fg_color='#101010', corner_radius=0)
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            self.root.rowconfigure(1, weight=0)
            self.root.pack(expand=True, fill='both')
            self.footer = self.create_footer()
            self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

            self.page = self.create_page((self.winfo_width(), self.winfo_height()))
            self.page.grid(column=0, row=0, sticky='nsew')

    def previous_page(self):
        if not self.settings_displayed and self.page_num > 0:
            self.page_num -= 1
            self.page = self.create_page((self.winfo_width(), self.winfo_height()))
            self.page.grid(column=0, row=0, sticky='nsew')
            self.footer = self.create_footer()
            self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

    def next_page(self):
        if not self.settings_displayed and self.page_num < self.total_pages - 1:
            self.page_num += 1
            self.page = self.create_page((self.winfo_width(), self.winfo_height()))
            self.page.grid(column=0, row=0, sticky='nsew')
            self.footer = self.create_footer()
            self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

    def create_settings_menu(self):
        menu = customtkinter.CTkFrame(self.root, corner_radius=5, fg_color='#1c1c1c')
        view_frame = customtkinter.CTkFrame(menu, fg_color='transparent')
        view_frame.grid_columnconfigure(0, weight=1)
        view_frame.grid_columnconfigure(2, weight=1)

        view_frame.grid_columnconfigure(1, weight=1)
        view_frame.grid_columnconfigure(3, weight=1)
        view_frame.grid_columnconfigure(4, weight=1)

        index = 0
        for category in get_all_categories():
            checkbox = customtkinter.CTkCheckBox(view_frame, text=category[1], onvalue=str(category[0]),
                                                 border_width=1, width=0, height=20,
                                                 checkbox_width=20, checkbox_height=20,
                                                 border_color='#555555')
            checkbox.grid(column=index % 5, row=index // 5, sticky='w', pady=1.5, padx=10)
            index += 1
        query_type = customtkinter.StringVar()
        query_type.set('AND')
        and_btn = customtkinter.CTkRadioButton(view_frame, text='and', variable=query_type, value='AND')
        and_btn.grid(column=3, row=index//5+1, pady=3.5, sticky='nsew')
        or_btn = customtkinter.CTkRadioButton(view_frame, text='or', variable=query_type, value='OR')
        or_btn.grid(column=4, row=index//5+1, pady=3.5, sticky='nsew')
        all_btn = customtkinter.CTkRadioButton(view_frame, text='all', variable=query_type, value='ALL')
        all_btn.grid(column=3, row=index//5+2, pady=3.5, sticky='nsew')

        submit = customtkinter.CTkButton(view_frame, text='save', width=40, command=partial(self.create_view, view_frame, query_type))
        submit.grid(column=4, row=index//5+2, sticky='nsew')

        view_frame.pack(expand=True, fill='both', pady=10, padx=10)
        return menu

    def create_view(self, frame, command: customtkinter.StringVar):
        category_list = []

        for child in frame.winfo_children():
            if isinstance(child, customtkinter.CTkCheckBox) and (cat_id := child.get()):
                category_list.append(cat_id)
        self.paths = create_new_view(category_list, command.get())
        if not self.paths:
            pass
        self.page_num = 0
        self.total_pages = ceil(len(self.paths) / 6)
        self.create_footer()
        self.create_page((self.winfo_width(), self.winfo_height()))
        self.settings()


    def create_page(self, wdw_size: tuple):
        if hasattr(self, 'page'):
            self.page.destroy()
        page = customtkinter.CTkFrame(self.root, fg_color='transparent')
        page.columnconfigure(0, weight=1)
        page.columnconfigure(1, weight=1)
        page.columnconfigure(2, weight=1)
        page.rowconfigure(0, weight=1)
        page.rowconfigure(1, weight=1)

        for index in range(6):
            row = 0
            column = index
            if column > 2:
                column -= 3
                row += 1
            try:
                path = self.paths[index+(self.page_num*6)]
                img_size = Image.open(path[1]).size
                image = customtkinter.CTkImage(Image.open(path[1]),
                                               size=self.img_scaling(img_size, wdw_size))
                photo = customtkinter.CTkButton(page, image=image, text='', fg_color='transparent', corner_radius=5)
                photo.configure(command=partial(self.describe, path, photo))
            except:
                photo = customtkinter.CTkFrame(page, height=(self.winfo_height()-self.footer.winfo_height())//2,
                                               width=self.winfo_width()//3, fg_color='transparent')
            photo.grid(column=column, row=row, sticky='nsew')
        return page

    def describe(self, path: tuple, button: customtkinter.CTkButton):
        window = Describe(self, path, button)
        button.configure(fg_color='#1f3f6b')
        window.grab_set()

    def resizer(self):
        self.page = self.create_page((self.winfo_width(), self.winfo_height()))
        self.page.grid(column=self.settings_displayed, row=0, sticky='nsew')

    def img_scaling(self, img_size: tuple, wdw_size: tuple):
        img_x, img_y = img_size
        wdw_x, wdw_y = wdw_size
        if self.settings_displayed:
            cell_x = (wdw_x - self.settings_menu.winfo_width()) / 3 - 20
        else:
            cell_x = wdw_x / 3 - 20

        cell_y = (wdw_y - self.footer.winfo_height()) / 2 - 20
        resize = min(cell_x / img_x, cell_y / img_y)
        final_size = (img_x * resize, img_y * resize)
        return final_size

    def close(self):
        config = read_config()
        config.set('BOOKMARKS', 'RECENT', str(self.page_num))
        with open('config.ini', 'w') as conf_file:
            config.write(conf_file)
        self.destroy()

if __name__ == '__main__':
    app = FileFinder()
    app.mainloop()
