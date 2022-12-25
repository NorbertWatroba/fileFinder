import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class Setup(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Setup")
        self.geometry("300x350")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.directory = customtkinter.CTkEntry(self.frame, placeholder_text="Directory name")
        self.directory.pack(padx=20, pady=(20, 10))

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
        with open('.env', 'w') as f:
            f.write(f'''ROOT = {self.directory.get()}

HOST = {self.host.get()}
DATABASE = {self.database.get()}
USER = {self.user.get()}
PASSWORD = {self.password.get()}''')


if __name__ == '__main__':
    setup = Setup()
    setup.mainloop()
