from __future__ import annotations

from dataclasses import dataclass
import re

# TODO: модели для: стринг, фикснам, флоат, аррей, хеш, регексп, структ, модуль  
@dataclass(frozen=True, slots=True, kw_only=True)
class RubyClass:
    name: str
    

@dataclass(slots=True, kw_only=True)
class RubyObject:
    cls_name: str
    attributes: dict

    def set_attributes(self, attrs: dict):
        self.attributes.update(attrs)


@dataclass(frozen=True, slots=True, kw_only=True)
class RubySymbol:
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
    
    
RubyTypes = RubyObject | str | int | float | list | dict | RubySymbol | re.Pattern | RubyClass | None | bool
    
