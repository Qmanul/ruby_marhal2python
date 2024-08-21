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
        self._write_bytes(symbol.encode())
        self._symbols.append(symbol)
        return None
        
    def _write_symblo_ref(self, index: int) -> None:
        self._write_bytes(Types.SYMBOLREF.value)
        self._write_bytes(index.to_bytes())
        return None

    def _write_object_ref(self, index) -> None:
        self._write_fixnum(index + 1)

    def _write_float(self, num: float) -> None:
        if num in self._objects:  # для этого бы написать отдельный метод/декоратор/функцию
            self._write_object_ref(self._objects.index(num))
            return None
        self._objects.append(num)

        num_string = str(num)
        self._write_fixnum(len(num_string))
        self._write_bytes(num_string.encode())
        return None 

    def _write_bignum(self, num: int):
        if num in self._objects:
            self._write_object_ref(self._objects.index(num))
            return None
        self._objects.append(num)

        self._write_bytes(Types.BIGNUM.value)
        if num > 0:
            self._write_bytes(b'+')
        else:
            self._write_bytes(b'-')

        length = ((num).bit_length() + 7) // 8
        self._write_fixnum(length // 2)
        for exp in range(length):
            self._write_bytes(((num >> (exp * 8)) & 0xFF).to_bytes())
        return None

    def _write_hash(self, hash: dict) -> None:
        if hash in self._objects:
            self._write_object_ref(self._objects.index(hash))
            return None
        self._objects.append(hash)

        self._write_bytes(Types.HASH.value)
        self._write_fixnum(len(hash))
        for key, value in hash.items():
            self._write_bytes(key)
            self._write_bytes(value)
        return None

    def _write_string(self, string: str) -> None:
        if string in self._objects:
            self._write_object_ref(self._objects.index(string))
            return None
        self._objects.append(string)

        self._write_fixnum(len(string))
        self._write_bytes(string.encode())

    def _write_user_defined(self) -> None:
        
        ...
    
    def write(self) -> BytesIO:  # type: ignore
        match self.obj:
            case float(num): self._write_float(num)
            case int(num): 
                if num >= 2 ** 30:
                    self._write_bignum(num)
                else:
                    self._write_fixnum(num)
            case str(s): self._write_string(s)


def dump(obj) -> BytesIO:
    return Writer(obj).write()