from customtkinter import CTk

from ui.gui.features.file_select.assembley.file_select_assembley import build as file_select_build
from ui.gui.features.map.assembley.map_assembley import build as map_build
from ui.gui.features.error.assembley.error_assembley import build as error_build
from ui.gui.routing.router import Router, Destination


class App:
    def __init__(self):

        # Вынести в отдельный метод
        self.root = CTk()
        self.root.title("Dummy")
        self.root.geometry(f"{1100}x{580}")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # это тоже
        self.router = Router()

        map_controller = map_build(self.root, self.router)
        file_select_controller = file_select_build(self.root, self.router)
        error_controller = error_build(self.root, self.router)

        self.router.add(Destination.MAP, map_controller)
        self.router.add(Destination.FILE_SELECT, file_select_controller)
        self.router.add(Destination.ERROR, error_controller)
        
    def start(self) -> None:
        self.router.navigate(Destination.FILE_SELECT)
        self.root.mainloop()


def app_start():
    App().start()
