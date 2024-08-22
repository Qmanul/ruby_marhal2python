import functools
from typing import Callable, Protocol, TypeVar

from .models import RubyTypes

__all__ = ['register_object']

F = TypeVar('F')


class HasObjectRegistry(Protocol):
    objects: list


def register_object(func: Callable[..., F]) -> Callable[..., F]:
    @functools.wraps(func)
    def wrapper(self: HasObjectRegistry) -> F:
        self.objects.append(None)
        index = len(self.objects) - 1
        res = func(self)
        self.objects[index] = res
        return res
    return wrapper 
