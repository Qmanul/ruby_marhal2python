from io import BytesIO
import math

from constants import MARSHAL_MAJOR_VERSION, MARSHAL_MINOR_VERSION, Types

class Writer:
    def __init__(self, obj) -> None:
        self.obj = obj
        self.output = BytesIO()
        self._symbols: list[str] = list()
        self._objects: list = list()
        self._write_marshal_version()
    
    def _write_bytes(self, data: bytes) -> None:
        self.output.write(data)
    
    def _write_marshal_version(self) -> None:
        self._write_bytes(MARSHAL_MAJOR_VERSION.to_bytes())
        self._write_bytes(MARSHAL_MINOR_VERSION.to_bytes())
        
    def _write_fixnum(self, num: int) -> None:
        self._write_bytes(Types.FIXNUM.value)
        if num == 0:
            self._write_bytes((0).to_bytes())
            return None
        if 1 <= num <= 122:
            self._write_bytes((num + 5).to_bytes())
            return None
        if -123 <= num <= -1:
            self._write_bytes((251 + num).to_bytes())
            return None
        
        size = math.ceil(num.bit_length() / 8)
        const = size if num >= 0 else 256 - size
        factor = 256 ** size
        if num < 0:
            if num * 256 == -factor:  # грязный хак   
                size -= 1
                const += 1
                num += factor // 256
            else:
                num += factor
        self._write_bytes(const.to_bytes())
        for _ in range(size):
            self._write_bytes((num % 256).to_bytes())
            num //= 256
        return None
            
    def _write_symbol(self, symbol: str) -> None:
        if symbol in self._symbols:
            self._write_symblo_ref(self._symbols.index(symbol))
            return None

        self._write_bytes(Types.SYMBOL.value)
        self._write_fixnum(len(symbol))
        self.write(symbol.encode())
        self._symbols.append(symbol)
        return None
        
    def _write_symblo_ref(self, index: int) -> None:
        self._write_bytes(Types.SYMBOLREF.value)
        self._write_bytes(index.to_bytes())
        return None

    def _write_float(self, num: float) -> None:
        self._objects.append(num)
        num = str(num)
        self._write_fixnum(len(num))
        self._write_bytes(num)
        return None 

    def _write_bignum(self, num: int):
        self._write_bytes(Types.BIGNUM.value)
        

    def _write_user_defined(self) -> None:
        
        ...
    
    def write(self) -> BytesIO:
        match self.obj:
            case float(num): self._write_float(num)
            case int(num): 
                if num > 100000:
                    self._write_bignum(num)
                else:
                    self._write_fixnum(num)


def dump(obj) -> BytesIO:
    return Writer(obj).write()