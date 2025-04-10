from __future__ import annotations
from typing import Callable

from customtkinter import CTk

from ui.gui.features.file_select.view.file_select_view import FileSelectView
from ui.gui.features.file_select.protocols import FileSelectPresenterProtocol


class FileSelectViewController:
    def __init__(self, root: CTk, presenter: FileSelectPresenterProtocol):
        self.view = FileSelectView(root)
        self.view.grid(row=0, column=0, sticky="nsew")
        self.presenter = presenter
        self.presenter.load_view(self, self.view)

    def set_select_button_clicked_handler(self, handler: Callable[[], None]) -> None:
        self.view.select_button.configure(command=handler)

    def set_confirm_button_clicked_handler(self, handler: Callable[[], None]) -> None:
        self.view.confirm_button.configure(command=handler)

    def set_confirm_button_state(self, state: str) -> None:
        self.view.confirm_button.configure(state=state)
    
    def set_filepath_label(self, filepath: str) -> None:
        self.view.filepath_label.configure(text=filepath)

    def open_file_dialog(self) -> str:
        return self.view._open_file_dialog()
