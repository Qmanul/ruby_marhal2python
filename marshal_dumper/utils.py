import functools
from typing import Callable, Protocol


__all__ = 'register_object', 'Registry'


class Registry[T]:
    def __init__(self) -> None:
        self.objects: list[T] = list()
        
    def add(self, obj: T) -> None:
        self.objects.append(obj)
        
    def get(self, index) -> T:
        return self[index]
    
    def __len__(self) -> int:
        return len(self.objects)

    def __getitem__(self, index) -> T:
        return self.objects[index]
    
    def __setitem__(self, index, value) -> None:
        self.objects[index] = value
        
    def append(self, obj: T) -> None:
        self.add(obj)
        

class HasObjectRegistry(Protocol):
    objects: Registry


def register_object[F](func: Callable[..., F]) -> Callable[..., F]:
    @functools.wraps(func)
    def wrapper(self: HasObjectRegistry) -> F:
        self.objects.append(None)
        index = len(self.objects) - 1
        res = func(self)
        self.objects[index] = res
        return res
    return wrapper 

    