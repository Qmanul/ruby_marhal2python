from enum import Enum
from typing import Protocol

from customtkinter import CTkFrame


class Destination(Enum):
    MAP = 'map'
    FILE_SELECT = 'file_select'
    ERROR = 'error'


class RouterProtocol(Protocol):
    def navigate(self, destination: Destination):
        ...

    def back(self):
        ...


class PresenterProtocol(Protocol):
    def signal(self, signal: dict[str, object]):
        ...


class ControllerProtocol(Protocol):
    view: CTkFrame
    presenter: PresenterProtocol


class Router:
    def __init__(self) -> None:
        self.controllers: dict[Destination, ControllerProtocol] = dict()
        self.previous: list[ControllerProtocol] = list()
        self.current: ControllerProtocol | None = None

    def add(self, destination: Destination, controller: ControllerProtocol) -> None:
        self.controllers.update({destination: controller})

    def navigate(self, destination: Destination, context = None) -> None:
        controller = self.controllers[destination]
        self.previous.append(self.current)
        self.current = controller
        controller.view.tkraise()
        
        if context:
            controller.presenter.signal(context)

    def back(self) -> None:
        try:
            previous_controller = self.previous.pop()
            self.current = previous_controller
            previous_controller.view.tkraise()
        except IndexError:
            pass
  