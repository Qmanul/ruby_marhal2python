from customtkinter import CTkFrame, CTkLabel, CTkButton, DISABLED, filedialog


class FileSelectView(CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0, 1,), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.filepath_label = CTkLabel(self, text='Select file...', )
        self.filepath_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.select_button = CTkButton(self, text='Open')
        self.select_button.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.confirm_button = CTkButton(self, text='Confirm', state=DISABLED)
        self.confirm_button.grid(row=1, column=1, sticky="nsew", pady=(10, 10), padx=(10, 10))

    def _open_file_dialog(self) -> str:
        return filedialog.askopenfilename(
            filetypes=(('All Files','*.*'),),
            title='Select File',
            initialdir='./',
        ) 
    