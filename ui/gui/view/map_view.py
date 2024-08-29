import typing
from customtkinter import CTkFrame, CTkScrollableFrame, CTkButton, CTkScrollbar, CTkProgressBar

from ui.gui.utils.ctk_both_way_scrollable_frame import CTkBothWayScrollableFrame


class Event(typing.Protocol):
    id: int
    name: str
    x: int
    y: int
    

class MapView(CTkFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        
        self.back_button = CTkButton(master=self, text="Back")
        self.back_button.grid(row=1, column=0, sticky="ew", pady=(10, 10), padx=(10, 10))
        
        # ----------------------------MAIN FRAME----------------------------------------------
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # ----------------------------MAP FRAME-----------------------------------------------
        self.map_frame = CTkBothWayScrollableFrame(self.main_frame)
        self.map_frame.grid(row=1, column=1, columnspan=3, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        self.map_events_frame = CTkFrame(self.map_frame)
        self.map_events_frame.grid(row=0, column=0, sticky="nsew")
        
        # ---------------------------EVENTS FRAME---------------------------------------------
        self.events_frame = CTkScrollableFrame(self.main_frame, label_text="Events")
        self.events_frame.grid(row=1, column=0, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.events_frame.grid_columnconfigure(0, weight=1)
        
        # ---------------------------TOOL BAR FRAME-------------------------------------------
        self.tool_bar_frame = CTkFrame(self.main_frame)
        self.tool_bar_frame.grid(row=0, column=0, pady=(10, 0), padx=(10, 10), columnspan=4, sticky="nsew")
        
        self.first_layer_button = CTkButton(self.tool_bar_frame, text='First')
        self.first_layer_button.grid(row=0, column=1, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.second_layer_button = CTkButton(self.tool_bar_frame, text='Second')
        self.second_layer_button.grid(row=0, column=2, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.third_layer_button = CTkButton(self.tool_bar_frame, text='Third')
        self.third_layer_button.grid(row=0, column=3, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        self.events_layer_button = CTkButton(self.tool_bar_frame, text='Events')
        self.events_layer_button.grid(row=0, column=4, sticky="nsew", pady=(10, 10), padx=(10, 10))
        
        # ----------------------------PROGRESS------------------------------------------------
        self.progress_frame = CTkFrame(self)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(0, weight=1)
        self.progress_frame.grid(row=0, column=0, sticky="nsew")
        
        self.progress = CTkProgressBar(self.progress_frame, mode='indeterminate')
        self.progress.grid(row=0, column=0, sticky="ew", pady=(10, 10), padx=(10, 10))
        self.progress.start()
    
    def clear(self):
        for c in tuple(self.events_frame.children.values()):
            c.destroy()
  
    def add_event(self, event: Event):
        button = CTkButton(master=self.events_frame, text=event.name)
        button.grid(column=0, padx=10, pady=(0, 20))
        map_button = CTkButton(master=self.map_events_frame, text=event.id, width=10, height=10)
        map_button.grid(row=event.y, column=event.x, padx=2, pady=2)
        
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
    
        