from __future__ import annotations
from typing import Callable, Protocol, ValuesView

from customtkinter import CTkButton

from rpgmaker_parser.models import RPGMap, RPGEvent



class MapPresenterProtocol(Protocol):
    def load_view(self, controller: MapViewControllerProtocol, view: MapViewProtocol) -> None:
        ...
    

class MapModelProtocol(Protocol):
    def process_rxdata(self, filepath: str) -> RPGMap:
        ...

    def get_events(self, map_ : RPGMap) -> ValuesView[RPGEvent]:
        ...


class MapViewProtocol(Protocol):
    ...


class MapViewControllerProtocol(Protocol):
    def set_back_button_handler(self, handler: Callable[[], None]) -> None:
        ...

    def schedule_action(self, action: Callable, delay = 100) -> None:
        ...

    def clear(self) -> None:        
        ...
  
    def add_event(self, event: RPGEvent) -> None:
        ...

    def show_progress(self) -> None:
        ...
        
    def hide_progress(self) -> None:
        ...
    