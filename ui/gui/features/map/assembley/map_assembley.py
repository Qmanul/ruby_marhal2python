from customtkinter import CTk

from ui.gui.features.map.model.map_model import MapModel
from ui.gui.features.map.presentation.map_presenter import MapPresenter
from ui.gui.features.map.protocols import MapViewControllerProtocol
from ui.gui.features.map.view.map_view_controller import MapViewController
from ui.gui.routing.router import RouterProtocol


def build(root: CTk, router: RouterProtocol) -> MapViewControllerProtocol:
    model = MapModel()
    presenter = MapPresenter(model, router)
    controller = MapViewController(root, presenter)
    return controller
    