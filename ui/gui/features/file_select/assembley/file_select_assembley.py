from customtkinter import CTk

from ui.gui.features.file_select.model.file_select_model import FileSelectModel
from ui.gui.features.file_select.presentation.file_select_presenter import FileSelectPresenter
from ui.gui.features.file_select.protocols import FileSelectViewControllerProtocol
from ui.gui.features.file_select.view.file_select_view_controller import FileSelectViewController#, FileSelectViewControllerProtocol
from ui.gui.routing.router import RouterProtocol


def build(root: CTk, router: RouterProtocol) -> FileSelectViewControllerProtocol:
    model = FileSelectModel()
    presenter = FileSelectPresenter(model, router)
    controller = FileSelectViewController(root, presenter)
    return controller
    