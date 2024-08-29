import typing
from concurrent.futures import ThreadPoolExecutor


class ViewManager(typing.Protocol):
    def switch_view(self, name: str, signal: typing.Mapping[str, object] | None = None) -> None:
        ...
        

class Model(typing.Protocol):
    def process_rxdata(self, filepath: str) -> object:
        ... 
    

class View(typing.Protocol):    
    def open_file_dialog(self) -> str:
        ...
        
    def confirm_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        ...
        
    def confirm_button_enable(self) -> None:
        ...
        
    def confirm_button_disable(self) -> None:
        ...
        
    def select_button_set_callback(self, callback: typing.Callable[[], None]) -> None:
        ...
    
    def filepath_set_text(self, text: str) -> None:
        ...
    
    def update(self) -> None:
        ...
        
    def progress_start(self) -> None:
        ...
        
    def progress_stop(self) -> None:
        ...


class FileSelectController:
    def __init__(self, view: View, model: Model, view_manager: ViewManager) -> None:
        self.view = view
        self.model = model
        self.view_manager = view_manager
        self.filepath: str | None = None
        self.set_callbacks()
    
    def set_callbacks(self):
        self.view.select_button_set_callback(self.select_file)
        self.view.confirm_button_set_callback(self.open_file)
        
    def open_file(self) -> None:
        if self.filepath is None or not self.filepath:
            return
        
        self.view.progress_start()
        
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.model.process_rxdata, self.filepath)
            
            while future.running():
                self.view.update()
            res = future.result()
        
        self.view.progress_stop()
        self.view_manager.switch_view('map', signal={'map': res})
                    
    def select_file(self) -> None:
        filepath = self.view.open_file_dialog()
        
        if not filepath:
            return
        
        self.filepath = filepath
        self.view.confirm_button_enable()
        self.view.filepath_set_text(filepath)
    
    def signal(self, signal: typing.Mapping[str, object]) -> None:
        match signal:
            case {'filepath': filepath} if filepath is not None:
                self.filepath = filepath
                self.view.confirm_button_enable()
                self.view.filepath_set_text(filepath)
                
            case {'clear': _}:
                self.filepath = None
                self.view.confirm_button_disable()
                self.view.filepath_set_text('Select file...')
        