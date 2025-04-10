from ui.gui.features.error.protocols import ErrorModelProtocol, ErrorViewControllerProtocol, ErrorViewProtocol
from ui.gui.routing.router import Destination, RouterProtocol
from ui.gui.utils.signal import Signal


class ErrorPresenter:
    def __init__(self, model: ErrorModelProtocol, router: RouterProtocol) -> None:
        self.model = model
        self.router = router
        self.view: ErrorViewProtocol | None = None
        self.view_controller: ErrorViewControllerProtocol | None = None

    def signal(self, signal: Signal):
        match signal:
            case Signal('message', message):
                self.view_controller.set_message(message)

            case Signal('clear'):
                self.view_controller.set_message('')

    def handle_back_button_clicked(self):
        self.signal(Signal('clear'))
        self.router.navigate(destination=Destination.FILE_SELECT)

    def set_handlers(self):
        self.view_controller.set_back_button_handler(self.handle_back_button_clicked)

    def load_view(self, controller: ErrorViewControllerProtocol, view: ErrorViewProtocol) -> None:
        self.view = view
        self.view_controller = controller
        self.set_handlers()
    