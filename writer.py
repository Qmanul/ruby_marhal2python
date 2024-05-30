from io import BytesIO
import math

from constants import MARSHAL_MAJOR_VERSION, MARSHAL_MINOR_VERSION, Types

class Writer:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.output = BytesIO()
        self._write_marshal_version()
    
    def _write_bytes(self, data: bytes) -> None:
        self.output.write(data)
    
    def _write_marshal_version(self) -> None:
        self._write_bytes(MARSHAL_MAJOR_VERSION.to_bytes())
        self._write_bytes(MARSHAL_MINOR_VERSION.to_bytes())
        
    def _write_fixnum(self, number: int) -> None:
        self._write_bytes(Types.FIXNUM.value)
        if number == 0:
            self._write_bytes((0).to_bytes())
            return None
        if 1 <= number <= 122:
            self._write_bytes((number + 5).to_bytes())
            return None
        if -123 <= number <= -1:
            self._write_bytes((251 + number).to_bytes())
            return None
        
        size = math.ceil(number.bit_length() / 8)
        const = size if number >= 0 else 256 - size
        factor = 256 ** size
        if number < 0:
            if number * 256 == -factor:  # грязный хак   
                size -= 1
                const += 1
                number += factor // 256
            else:
                number += factor
        self._write_bytes(const.to_bytes())
        for _ in range(size):
            self._write_bytes((number % 256).to_bytes())
            number //= 256
        return None
            
        
    def _write_symbol(self, symbol: str) -> None:
        self._write_bytes(Types.SYMBOL.value)
        
        ...
        
    def _write_symblo_ref(self, index: int) -> None:
        ...
        
    def _write_user_defined(self) -> None:
        
        ...
    
    def write(self) -> BytesIO:
        if self.obj.__module__ == object.__module__:
            ...
        else:
            ...
        return self.output


def dump(obj) -> BytesIO:
    return Writer(obj).write()