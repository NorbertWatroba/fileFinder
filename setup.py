import customtkinter
from dbCreator import create_db
from configparser import ConfigParser


class Setup(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Setup")
        self.geometry("250x350")
        self.resizable(False, False)

        self.root = customtkinter.CTkFrame(self, fg_color='#101010', corner_radius=0)
        self.root.pack(expand=True, fill='both')

        self.frame = customtkinter.CTkFrame(self.root, fg_color='#1c1c1c')
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.path = customtkinter.CTkEntry(self.frame, placeholder_text="Absolute path to directory")
        self.path.pack(padx=20, pady=(20, 10))

        self.host = customtkinter.CTkEntry(self.frame, placeholder_text="Host")
        self.host.pack(padx=20, pady=10)

        self.database = customtkinter.CTkEntry(self.frame, placeholder_text="Database")
        self.database.pack(padx=20, pady=10)

        self.user = customtkinter.CTkEntry(self.frame, placeholder_text="User")
        self.user.pack(padx=20, pady=10)

        self.password = customtkinter.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.password.pack(padx=20, pady=(10, 20))

        self.submit = customtkinter.CTkButton(self.frame, text="Save", command=self.create_env)
        self.submit.pack(padx=20, pady=(10, 20))

    def create_env(self):
        config = ConfigParser()
        directory = self.path.get().split('\\')[-1]
        path = '\\'.join(self.path.get().split('\\')[:-1])
        config['OS'] = {'DIRECTORY': directory,
                        'ABSOLUTE_PATH': path}
        config['DATABASE'] = {'HOST': self.host.get(),
                              'DATABASE': self.database.get(),
                              'USER': self.user.get(),
                              'PASSWORD': self.password.get()}
        config['BOOKMARKS'] = {'RECENT': 0}
        with open('config.ini', 'w') as conf_file:
            config.write(conf_file)
        create_db()
        self.destroy()


if __name__ == '__main__':
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    setup = Setup()
    setup.mainloop()
