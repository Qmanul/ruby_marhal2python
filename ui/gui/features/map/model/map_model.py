from typing import ValuesView

from rpgmaker_parser.models import RPGEvent, RPGMap
from rpgmaker_parser.reader import load_from_file
from ui.gui.exceptions import InvalidMapException


class MapModel: 
    def process_rxdata(self, filepath: str) -> RPGMap:
        self._check_file_format(filepath)
        map_ = load_from_file(filepath)
        if isinstance(map_, RPGMap):
            return map_
        
        raise InvalidMapException(f'Invalid map file: {filepath}')
    
    def _check_file_format(self, filepath: str) -> None:
        if not filepath.endswith('.rxdata'):
            raise InvalidMapException(f'Invalid file extension: {filepath[filepath.find("."):]}')
