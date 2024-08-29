from collections.abc import ValuesView

from rpgmaker_parser.models import RPGEvent, RPGMap, RubyObject
from rpgmaker_parser.reader import load

class Model:
    def process_rxdata(self, filepath: str) -> RubyObject:
        with open(filepath, 'rb') as file:
            return load(file)
        
    def get_events(self, map_ : RPGMap) -> ValuesView[RPGEvent]:
        return map_.events.values()
    