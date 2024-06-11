from __future__ import annotations

from dataclasses import dataclass
import re
from typing import ClassVar
from collections.abc import ItemsView


# TODO: модели для: стринг, фикснам, флоат, аррей, хеш, регексп, структ, модуль  
@dataclass(frozen=True, slots=True)
class RubyClass:
    name: str

    def __hash__(self) -> int:
        return hash(self.name)
    

@dataclass(slots=True, kw_only=True)
class RubyObject:
    cls_name: str
    attributes: dict

    def set_attributes(self, attrs: dict):
        self.attributes.update(attrs)


@dataclass(frozen=True, slots=True)
class RubyString:
    name: str

    def __getitem__(self, item: int | slice) -> str:
        return self.name[item]

    def __len__(self) -> int:
        return len(self.name)

    def __bool__(self) -> bool:
        return bool(self.name)

    def startswith(self, *queries: str) -> bool:
        return self.name.startswith(queries)

    def endswith(self, *queries: str) -> bool:
        return self.name.endswith(queries)

    def is_empty(self) -> bool:
        return not bool(self)

    def __hash__(self) -> int:
        return hash(self.name)
    

@dataclass(frozen=True, slots=True)
class RubySymbol(RubyString):
    register: ClassVar[dict[str, RubySymbol]] = dict()

    # ёюанный руби с его мета программированием
    def __new__(cls, **kwargs) -> RubySymbol:
        if (symb := cls.register.get(kwargs['name'])) is not None:
            return symb
        return super().__new__(cls)

    def __post_init__(self) -> None:
        self.__class__.register.update({self.name: self})

    @classmethod
    def all_symbols(cls) -> ItemsView[str, RubySymbol]:
        return cls.register.items()


RubyFloat = float
RubyFixnum = int
nil = None
true = True
false = False
    
RubyTypes = RubyObject | str | int | float | list | dict | RubySymbol | re.Pattern | RubyClass | None | bool
