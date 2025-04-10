from __future__ import annotations

from typing import Protocol, Callable


# Куда деть протоколы


class ErrorModelProtocol(Protocol):
    ...


class ErrorViewProtocol(Protocol):
    ...


class ErrorViewControllerProtocol(Protocol):
    view: ErrorViewProtocol
    presenter: ErrorPresenterProtocol

    def set_message(self, message: str) -> None:
        ...

    def set_back_button_handler(self, handler: Callable[[], None]) -> None:
        ...

class ErrorPresenterProtocol(Protocol):
    def load_view(self, controller: ErrorViewControllerProtocol, view: ErrorViewProtocol) -> None:
        ...
