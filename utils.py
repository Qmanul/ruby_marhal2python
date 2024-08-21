import functools
from typing import Callable, Protocol

from models import RubyTypes

__all__ = ['register_object']


class HasObjectRegistry(Protocol):
    objects: list


def register_object(func: Callable[..., RubyTypes]) -> Callable[..., RubyTypes]:
    @functools.wraps(func)
    def wrapper(self: HasObjectRegistry) -> RubyTypes:
        self.objects.append(None)
        index = len(self.objects) - 1
        res = func(self)
        self.objects[index] = res
        return res
    return wrapper 
