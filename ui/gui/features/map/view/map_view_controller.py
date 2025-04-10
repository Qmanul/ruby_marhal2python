from typing import Callable
from customtkinter import CTk, CTkButton

from rpgmaker_parser.models import RPGEvent
from ui.gui.features.map.protocols import MapPresenterProtocol
from ui.gui.features.map.view.map_view import MapView
    

class MapViewController:
    def __init__(self, root: CTk, presenter: MapPresenterProtocol):
        self.view = MapView(root)
        self.view.grid(row=0, column=0, sticky="nsew")
        self.presenter = presenter
        self.presenter.load_view(self, self.view)

    def clear(self):        
        for c in (*self.view.events_frame.winfo_children(), *self.view.map_events_frame.winfo_children()):
            c.destroy()
  
    def add_event(self, event: RPGEvent) -> None:
        CTkButton(self.view.map_events_frame, text=event.id, width=10, height=10).grid(row=event.y, column=event.x, padx=2, pady=2)
        CTkButton(self.view.events_frame, text=event.name).grid(column=0, padx=10, pady=(0, 20))

    def set_back_button_handler(self, handler: Callable[[], None]) -> None:
        self.view.back_button.configure(command=handler)
    
    def schedule_action(self, action: Callable, delay = 100) -> None:
        self.view.after(delay, action)

    def show_progress(self) -> None:
        self.view.progress_frame.grid()
        self.view.main_frame.grid_remove()
        
    def hide_progress(self) -> None:
        self.view.progress_frame.grid_remove()
        self.view.main_frame.grid()
