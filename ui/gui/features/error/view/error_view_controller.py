from customtkinter import CTk
from typing import Callable

from ui.gui.features.error.protocols import ErrorPresenterProtocol
from ui.gui.features.error.view.error_view import ErrorView


class ErrorViewController:
    def __init__(self, root: CTk, presenter: ErrorPresenterProtocol):
        self.view = ErrorView(root)
        self.view.grid(row=0, column=0, sticky="nsew")
        self.presenter = presenter
        self.presenter.load_view(self, self.view)

    def set_message(self, message: str) -> None:
        self.view.label.configure(text=message)

    def set_back_button_handler(self, handler: Callable[[], None]) -> None:
        self.view.back_button.configure(command=handler)
