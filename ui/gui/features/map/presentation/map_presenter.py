from multiprocessing import Process, Queue

from rpgmaker_parser.models import RPGEvent, RPGMap
from ui.gui.exceptions import InvalidMapException
from ui.gui.features.map.protocols import MapModelProtocol, MapViewControllerProtocol, MapViewProtocol
from ui.gui.routing.router import Destination, RouterProtocol
from ui.gui.utils.signal import Signal


class MapPresenter:
    def __init__(self, model: MapModelProtocol, router: RouterProtocol) -> None:
        self.model = model
        self.router = router
        self.view: MapViewProtocol | None = None
        self.view_controller: MapViewControllerProtocol | None = None
        self.process: Process | None = None
        self.queue: Queue[RPGEvent] = Queue()

    def signal(self, signal: Signal):
        match signal:
            case Signal('filepath', filepath):
                self.signal(Signal('clear'))
                self.signal(Signal('show_progress'))

                try:
                    map_ = self.model.process_rxdata(filepath)

                except Exception as e:
                    self.router.navigate(Destination.ERROR, Signal('message', f'{e.__class__.__name__}: {str(e)}'))
                    return
                
                self.process = Process(target=self.process_map, args=(map_, self.queue), daemon=True)
                self.view_controller.schedule_action(self.check_process_alive, 100)
                self.process.start()

            case Signal('clear'):
                self.view_controller.clear()

            case Signal('show_progress'):
                self.view_controller.show_progress()

            case Signal('hide_progress'):
                self.view_controller.hide_progress()

    def process_map(self, map_: RPGMap, q: Queue) -> None:
        for e in map_.events.values():
            q.put(e)

    def check_process_alive(self) -> None:
        while not self.queue.empty():
            self.view_controller.add_event(self.queue.get())
        
        if not self.process.is_alive():
            self.signal(Signal('hide_progress'))
            return
        
        self.view_controller.schedule_action(self.check_process_alive, 100)

    def handle_back_button_clicked(self):
        if self.process and self.process.is_alive():
            self.process.terminate()
        self.router.back()

    def set_handlers(self):
        self.view_controller.set_back_button_handler(self.handle_back_button_clicked)

    def load_view(self, controller: MapViewControllerProtocol, view: MapViewProtocol) -> None:
        self.view = view
        self.view_controller = controller
        self.set_handlers()
    