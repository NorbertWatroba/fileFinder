import customtkinter
from PIL import Image

from functools import partial
from math import ceil

from utils import size_scaling
from queries import get_all_paths
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

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.pack(expand=True, fill='both')

        # collecting data
        self.paths = get_all_paths()
        self.page_num = 0
        self.total_pages = ceil(len(self.paths) / 6)

        # building home page
        self.page = self.create_page((700, 450))
        self.page.grid(column=0, row=0, sticky='nsew')

        self.footer = self.create_footer()
        self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

        # binds definition
        self.bind('<KeyPress-F5>', self.resizer)
        self.bind('<KeyPress-Right>', self.next_page)
        self.bind('<KeyPress-Left>', self.previous_page)

    def next_page(self, *args):
        if self.page_num < self.total_pages - 1:
            self.page_num += 1
            self.page = self.create_page((self.winfo_width(), self.winfo_height()))
            self.page.grid(column=0, row=0, sticky='nsew')
            self.footer = self.create_footer()
            self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

    def previous_page(self, *args):
        if self.page_num > 0:
            self.page_num -= 1
            self.page = self.create_page((self.winfo_width(), self.winfo_height()))
            self.page.grid(column=0, row=0, sticky='nsew')
            self.footer = self.create_footer()
            self.footer.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

    def create_page(self, wdw_size):
        page = customtkinter.CTkFrame(self.root, fg_color='transparent')
        page.grid_columnconfigure(0, weight=1)
        page.grid_columnconfigure(1, weight=1)
        page.grid_columnconfigure(2, weight=1)
        page.grid_rowconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1)

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
                                               size=size_scaling(img_size, wdw_size))
                photo = customtkinter.CTkButton(page, image=image, text='', fg_color='transparent', corner_radius=5,
                                                command=partial(self.describe, path))
            except:
                photo = customtkinter.CTkFrame(page, height=(self.winfo_height()-65)//2,
                                               width=self.winfo_width()//3, fg_color='transparent')
            photo.grid(column=column, row=row, sticky='nsew')
        return page

    def resizer(self, *args):
        self.page = self.create_page((self.winfo_width(), self.winfo_height()))
        self.page.grid(row=0, sticky='nsew')

    def create_footer(self):
        footer = customtkinter.CTkFrame(self.root, corner_radius=5, fg_color='#1c1c1c')
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=0)
        footer.columnconfigure(2, weight=1)
        text = customtkinter.CTkLabel(footer,
                                      text=f'   {self.page_num + 1} / {self.total_pages}   ', height=65)
        text.grid(column=1, row=0)
        btn_f = customtkinter.CTkButton(footer, text='>', command=self.next_page, width=20, height=20)
        btn_f.grid(column=2, row=0, sticky='w')
        btn_p = customtkinter.CTkButton(footer, text='<', command=self.previous_page, width=20, height=20)
        btn_p.grid(column=0, row=0, sticky='e')
        return footer

    @staticmethod
    def describe(path: tuple):
        Describe(path).mainloop()


app = FileFinder()
app.mainloop()
