from dataclasses import dataclass


@dataclass
class Signal:
    name: str
    value: object = None
