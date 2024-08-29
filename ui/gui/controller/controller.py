import typing

class SubController(typing.Protocol):
    def signal(self, signal: dict[str, object]) -> None:
        ...


class Root(typing.Protocol):
    def mainloop(self) -> None:
        ...


class Frame(typing.Protocol):
    def __init__(self, root: Root) -> None:
        ...
    
    def grid(self, *args, **kwargs) -> None:
        ...
        
    def tkraise(self) -> None:
        ...
        
        
class View(typing.NamedTuple):
    frame: Frame
    controller: SubController


class Controller:
    def __init__(self, root: Root, model) -> None:
        self.root = root
        self.model = model
        self.view_registry: dict[str, View] = dict()
        self.home_name: str | None = None

    def register_view(
        self, 
        name: str, 
        frame_cls: typing.Type[Frame], 
        controller_cls: typing.Type[SubController],
        home=False
        ):
        frame = frame_cls(self.root)
        frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        controller = controller_cls(frame, self.model, self)
        self.view_registry.update({name: View(frame, controller)})
        if home:
            self.home_name = name
        
    def switch_view(self, name: str, signal: typing.Mapping[str, object] | None = None) -> None:
        if (view := self.view_registry.get(name)) is not None:
            view.frame.tkraise()
            if signal:
                view.controller.signal(signal)
        
    def start(self):
        if self.home_name:
            self.switch_view(self.home_name)
        self.root.mainloop()
        