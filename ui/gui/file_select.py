import customtkinter


class FileSelect(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1,), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.label = customtkinter.CTkLabel(self, text="File Select")
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
        self.button = customtkinter.CTkButton(self, text="Select File", command=self.open_file)
        self.button.grid(row=1, column=0, padx=20, pady=20)
        self.button_confirm = customtkinter.CTkButton(self, text="Confirm", command=self.confirm)
        self.button_confirm.grid(row=1, column=1, padx=20, pady=20)
        
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.configure(mode="indeterminnate")
    
    def open_file(self) -> str:
        filename = customtkinter.filedialog.askopenfilename(
            filetypes=(
                ('RPG Maker XP Files', '*.rxdata'),
                ),
            title='Select File',
            initialdir='./',
            parent=self,
        )
        if not filename:
            return
        self.label.configure(text=filename)
        
    def confirm(self):
        print(self.label.cget('text'))    
        self.progressbar.grid(row=2, column=0, columnspan=2, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar.start()
        