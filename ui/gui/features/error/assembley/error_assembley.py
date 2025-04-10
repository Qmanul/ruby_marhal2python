from customtkinter import CTk


from ui.gui.features.error.protocols import ErrorViewControllerProtocol
from ui.gui.routing import router
from ui.gui.features.error.model.error_model import ErrorModel
from ui.gui.features.error.presentation.error_presenter import ErrorPresenter
from ui.gui.features.error.view.error_view_controller import ErrorViewController


def build(root: CTk, router: router.RouterProtocol) -> ErrorViewControllerProtocol:
    model = ErrorModel()
    presenter = ErrorPresenter(model, router)
    controller = ErrorViewController(root, presenter)
    return controller
    