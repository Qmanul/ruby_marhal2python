from ui.gui.controller.controller import Controller
from ui.gui.controller.map_controller import MapController
from ui.gui.model.model import Model
from ui.gui.controller.file_select_controller import FileSelectController
from ui.gui.view.file_select_view import FileSelectView
from ui.gui.view.map_view import MapView
from ui.gui.view.root import Root
    
    
class App:
    def __init__(self) -> None:
        self.controller = Controller(Root(), Model())
        self.controller.register_view('file_select', FileSelectView, FileSelectController, home=True)
        self.controller.register_view('map', MapView, MapController)
        self.start()

    def start(self):
        self.controller.start()
    