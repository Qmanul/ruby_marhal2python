import typing
import customtkinter


class Map(typing.Protocol):
    
    ...


class FileSelect(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1,), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

    def draw_map(self, map: Map):
        pass
    