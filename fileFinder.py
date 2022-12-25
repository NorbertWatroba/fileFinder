import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("fileFinder")
        self.geometry("700x450")

        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.settings = customtkinter.CTkFrame(self)


if __name__ == '__main__':
    app = App()
    app.mainloop()
