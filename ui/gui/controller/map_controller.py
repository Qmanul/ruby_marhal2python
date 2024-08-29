from collections.abc import ValuesView
import typing

from rpgmaker_parser.models import RPGEvent, RPGMap


class ViewManager(typing.Protocol):
    def switch_view(self, name: str, signal: typing.Mapping[str, object] | None = None) -> None:
        ...
        

class Model(typing.Protocol):
    def get_events(self, map_ : RPGMap) -> ValuesView[RPGEvent]:
        ...
    

class View(typing.Protocol):    
    def add_event(self, events: RPGEvent):
        ...
        
    def back_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        ...
        
    def update(self) -> None:
        ...
        
    def clear(self) -> None:
        ...
        
    def show_progress(self) -> None:
        ...
        
    def hide_progress(self) -> None:
        ...
        
    def in_progress(self) -> bool:
        ...


class MapController:
    def __init__(self, view: View, model: Model, view_manager: ViewManager) -> None:
        self.view = view
        self.model = model
        self.view_manager = view_manager
        self.set_callbacks()
        self.cancel = False
    
    def set_callbacks(self):
        self.view.back_button_set_callback(self.back)
    
    def back(self) -> None:
        self.cancel = True
        self.signal({'clear': None})
        self.view_manager.switch_view('file_select')
    
    def signal(self, signal: typing.Mapping[str, object]) -> None:
        match signal:
            case {'map': map_} if map_ is not None:
                events = self.model.get_events(map_)
                self.view.show_progress()
                for event in events:
                    if self.cancel:
                        self.cancel = False
                        break
                    self.view.add_event(event)
                    self.view.update()
                self.view.hide_progress()
                
            case {'clear': None}:
                self.view.clear()
                if self.cancel and not self.view.in_progress():
                    self.cancel = False