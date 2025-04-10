from customtkinter import CTkFrame, CTkLabel, CTkButton


class ErrorView(CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label = CTkLabel(self)
        self.label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))

        self.back_button = CTkButton(self, text="Back")
        self.back_button.grid(row=1, column=0, sticky="ew", pady=(10, 10), padx=(10, 10))
        