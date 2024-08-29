import typing
import customtkinter  # type: ignore


class FileSelectView(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure((0, 1,), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.filepath_label = customtkinter.CTkLabel(self, text='Select file...', )
        self.filepath_label.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.select_button = customtkinter.CTkButton(self, text='Open')
        self.select_button.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.confirm_button = customtkinter.CTkButton(self, text='Confirm', state=customtkinter.DISABLED)
        self.confirm_button.grid(row=1, column=1, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.progress = customtkinter.CTkProgressBar(self, mode='indeterminate')
        self.progress.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.progress.start()
        self.progress.grid_remove()
    
    def progress_start(self) -> None:
        self.progress.grid()
        
    def progress_stop(self) -> None:
        self.progress.grid_forget()
    
    def confirm_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        self.confirm_button.configure(command=callback)
        
    def select_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        self.select_button.configure(command=callback)
        
    def confirm_button_enable(self) -> None:
        self.confirm_button.configure(state=customtkinter.NORMAL)
        
    def confirm_button_disable(self) -> None:
        self.confirm_button.configure(state=customtkinter.DISABLED)
        
    def filepath_set_text(self, text: str) -> None:
        self.filepath_label.configure(text=text)
    
    def open_file_dialog(self) -> str:
        return customtkinter.filedialog.askopenfilename(
            filetypes=(('All Files','*.*'),),
            title='Select File',
            initialdir='./',
        )   