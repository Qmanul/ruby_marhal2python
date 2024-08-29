import typing
import customtkinter  # type: ignore


class Event(typing.Protocol):
    id: int
    name: str
    

class MapView(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.events: list[customtkinter.CTkButton] = list()
        self.events_frame = customtkinter.CTkScrollableFrame(self.main_frame, label_text="Events")
        self.events_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.events_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_frame = customtkinter.CTkFrame(self)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(0, weight=1)
        self.progress_frame.grid(row=0, column=0, sticky="nsew")
        
        self.progress = customtkinter.CTkProgressBar(self.progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.progress.start()
        
        self.back_button = customtkinter.CTkButton(master=self, text="Back")
        self.back_button.grid(row=1, column=0, sticky="ew", pady=(10, 10), padx=(10, 10))
        
    def clear(self):
        self.events_frame.destroy()
        self.events_frame = customtkinter.CTkScrollableFrame(self.main_frame, label_text="Events")
        self.events_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.events_frame.grid_columnconfigure(0, weight=1)
  
    def add_event(self, event: Event):
        button = customtkinter.CTkButton(master=self.events_frame, text=event.name)
        button.grid(row=len(self.events), column=0, padx=10, pady=(0, 20))
        self.events.append(button)
        
    def back_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        self.back_button.configure(command=callback)
        
    def show_progress(self) -> None:
        self.progress_frame.grid()
        self.main_frame.grid_remove()
        
    def hide_progress(self) -> None:
        self.progress_frame.grid_remove()
        self.main_frame.grid()
    
    def in_progress(self) -> bool:
        return bool(self.progress_frame.grid_info())
        