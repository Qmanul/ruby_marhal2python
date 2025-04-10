from __future__ import annotations

from customtkinter import NORMAL

from ui.gui.features.file_select.protocols import FileSelectModelProtocol, FileSelectViewControllerProtocol, FileSelectViewProtocol
from ui.gui.routing.router import Destination, RouterProtocol
from ui.gui.utils.signal import Signal


class FileSelectPresenter:
    def __init__(self, model: FileSelectModelProtocol, router: RouterProtocol) -> None:
        self.model = model
        self.router = router
        self.view: FileSelectViewProtocol | None = None
        self.view_controller: FileSelectViewControllerProtocol | None = None
    
    def handle_select_button_clicked(self) -> None:
        filepath = self.view_controller.open_file_dialog()
        if not filepath:
            return
        self.signal(Signal('filepath', filepath))

    def handle_confirm_button_clicked(self) -> None:
        self.router.navigate(Destination.MAP, Signal('filepath', self.model.filepath))
        
    def set_handlers(self) -> None:
        self.view_controller.set_select_button_clicked_handler(self.handle_select_button_clicked)
        self.view_controller.set_confirm_button_clicked_handler(self.handle_confirm_button_clicked)

    def signal(self, signal: Signal) -> None:
        match signal:
            case Signal('filepath', filepath):
                self.view_controller.set_filepath_label(filepath)
                self.view_controller.set_confirm_button_state(NORMAL)
                self.model.filepath = filepath
                
            case Signal('clear', _):
                self.view_controller.set_filepath_label('Select file...')
                self.view_controller.set_confirm_button_state(NORMAL)
                self.model.filepath = None

    def load_view(self, controller: FileSelectViewControllerProtocol, view: FileSelectViewProtocol) -> None:
        self.view = view
        self.view_controller = controller
        self.set_handlers()
