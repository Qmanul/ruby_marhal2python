from __future__ import annotations

from typing import Protocol, Callable


# Куда деть протоколы


class FileSelectModelProtocol(Protocol):
    filepath: str


class FileSelectViewProtocol(Protocol):
    ...


class FileSelectViewControllerProtocol(Protocol):
    view: FileSelectViewProtocol
    presenter: FileSelectPresenterProtocol

    def set_select_button_clicked_handler(self, handler: Callable[[], None]) -> None:
        ...

    def set_confirm_button_clicked_handler(self, handler: Callable[[], None]) -> None:    
        ...

    def set_confirm_button_state(self, state: str) -> None:
        ...

    def open_file_dialog(self) -> str:
        ...

    def set_filepath_label(self, filepath: str) -> None:
        ...


class FileSelectPresenterProtocol(Protocol):
    def load_view(self, controller: FileSelectViewControllerProtocol, view: FileSelectViewProtocol) -> None:
        ...
