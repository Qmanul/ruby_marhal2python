from __future__ import annotations

import re
import collections
from typing import BinaryIO, NoReturn

from .models import RubyClass, RubySymbol, RubyObject, RubyTypes
from .exception import VersionError, TypeNotSupportedError
from .constants import Types, MARSHAL_MAJOR_VERSION, MARSHAL_MINOR_VERSION
from .utils import register_object

__all__ = ['load', 'load_from_file']


class _Reader:
    __slots__ = 'stream', 'symbols', 'objects'
    def __init__(self, stream: BinaryIO) -> None:
        self.stream = stream
        self.check_marshal_version()
        self.objects: list[RubyTypes] = list()
        self.symbols: list[RubySymbol] = list()  # почему у символов отдельная таблица ??? 
        
    def check_marshal_version(self) -> None | NoReturn:  # я тут выёбывыаюсь знанием типов (посмотрел 1 видео)
        major_version = ord(self.read_bytes())
        minor_version = ord(self.read_bytes())
        if major_version != MARSHAL_MAJOR_VERSION or minor_version > MARSHAL_MINOR_VERSION:
            raise VersionError(f'{MARSHAL_MAJOR_VERSION}.{MARSHAL_MINOR_VERSION}',
                               f'{major_version}.{minor_version}')
        return None
    
    # метод шобы не писать self._stream.read(ln)
    def read_bytes(self, ln: int = 1) -> bytes:
        return self.stream.read(ln)

    def read_symbol(self) -> RubySymbol:
        symb = RubySymbol(name=self.read_bytes(self.read_fixnum()).decode())
        self.symbols.append(symb)
        return symb

    def read_symbol_ref(self) -> RubySymbol:
        return self.symbols[self.read_fixnum()]

    def read_fixnum(self) -> int:
        ln = ord(self.read_bytes())
        if 6 <= ln <= 127:
            return ln - 5
        if 128 <= ln <= 250:
            return ln - 251  # ???? кто это нахуй придумал???? почему 251???? а блять потому что 256 - 5 ну ахуеть

        const = 0 if ln <= 4 else 256  # понятия не имею как назвать переменную пусть буит const
        return sum((ord(self.read_bytes()) - const) * 256 ** exp for exp in range(abs(const - ln)))

    def read_object_ref(self) -> RubyTypes:
        return self.objects[self.read_fixnum() - 1]  # почему индекс объектов начинается с 1, тогда как символов с 0 ???

    @register_object
    def read_regexp(self) -> re.Pattern:
        pattern = self.read_bytes(self.read_fixnum()).decode('US-ASCII')
        flags = ord(self.read_bytes())
        options = sum(re_flag for flag, re_flag in {1: re.I, 2: re.X, 4: re.S}.items() if flags & flag)  # спасибо tabnine
        return re.compile(pattern, options)

    @register_object
    def read_string(self) -> str:
        return self.read_bytes(self.read_fixnum()).decode()

    # ну и залупа кто это придумал
    @register_object
    def read_ivar(self) -> RubyTypes:
        
        type_byte = Types(self.read_bytes())
        if type_byte is Types.STRING:
            s = self.read_bytes(self.read_fixnum())
            
        elif type_byte is Types.REGEXP:
            s = self.read_bytes(self.read_fixnum())
            flags = ord(self.read_bytes())
            options = sum(re_flag for flag, re_flag in {1: re.I, 2: re.X, 4: re.S}.items() if flags & flag)
            
        elif type_byte in (Types.USERDEFINED, Types.USERCLASS): 
            o = self.read_user_defined() if type_byte is Types.USERDEFINED else self.read_user_class()
            o.set_attributes(self.read_attributes())  # type: ignore
            return o
        
        else:
            raise TypeNotSupportedError(type_byte.name)
               
        attrs = self.read_attributes()
        encoding = attrs.get('E', attrs.get('encoding'))
        if encoding is True:
            encoding = 'UTF-8'
        if encoding is False:
            encoding = 'US-ASCII'
        try:
            res = s.decode(encoding)
        except UnicodeDecodeError as e:
            print(f'Something went wrong while decoding a string: {e.reason}\nDefaulting to UTF-8')
            res = s.decode('UTF-8')
            
        if type_byte is Types.REGEXP:
            res = re.compile(res, options)  #type: ignore
        return res

    def read_extended(self):
        self.read_symbol()  # нам особо нет дела до имени модуля
        return self.parse()

    @register_object
    def read_array(self) -> list:
        return [self.parse() for _ in range(self.read_fixnum())]

    @register_object
    def read_bignum(self) -> int:
        sign = self.read_bytes().decode()  # '+' | '-'
        data = self.read_bytes(self.read_fixnum() * 2)  # зачем надо было делить длину на 2 :FaunaTired:
        # https://ruby-doc.org/3.2.2/marshal_rdoc.html#label-Bignum
        res = 0
        for exp, byte in enumerate(data):
            res |= byte << (exp * 8)  # спасибо tabnine
        if sign == '-':
            res = -res
        return res

    @register_object
    def read_class(self) -> RubyClass:
        return RubyClass(name=self.read_bytes(self.read_fixnum()).decode())

    # вроде можно дампить, но там как то хитровыебанно поэтому пока просто кидаем ошибку мб когда-нибудь сделаю
    def read_data(self):
        raise TypeNotSupportedError('Data')

    @register_object
    def read_float(self) -> float:
        return float(self.read_bytes(self.read_fixnum()))  # 0.0, NaN, inf, -inf

    def _read_hash(self) -> dict:
        return {self.parse(): self.parse() for _ in range(self.read_fixnum())}
    
    @register_object
    def read_hash(self) -> dict:
        return self._read_hash()

    # почему ты есть
    @register_object
    def read_hash_w_default_value(self) -> dict:
        # Сначала читаем хеш потому что дефолт валью в конце. Очень удобно спасибо руби
        h = self._read_hash()
        # я так счастлив я так рад у меня есть дефолтдикт, хочу сказать благодарю и говорю "соси"
        # соси благодраю тебя, соси спасибо, что ты есть
        # ну а не серьёзной ноте, я хз если это работает с объектами
        return collections.defaultdict(lambda: self.parse(), h)

    @register_object
    def read_object(self) -> RubyObject:
        return RubyObject(cls_name=self.read_symbol_name(), attributes=self.read_attributes())

    @register_object
    def read_struct(self) -> RubyObject:
        return RubyObject(cls_name=self.read_symbol_name()[8:], attributes=self.read_attributes())  # [8:] отсекает 'Struct::'

    # 3 метода ниже это ёбанное богохульство я не буду их имплементить
    # upd: ладно хуй с ним
    @register_object
    def read_user_defined(self) -> RubyObject:
        return RubyObject(cls_name=self.read_symbol_name(), attributes={"data":self.read_bytes(self.read_fixnum())})
    
    @register_object
    def read_user_class(self) -> RubyObject:
        return RubyObject(cls_name=self.read_symbol_name(), attributes={'data': self.parse()}) 
    
    def read_attributes(self) -> dict:
        return {self.read_symbol_name(): self.parse() for _ in range(self.read_fixnum())}
    
    # метод штобы mypy не ругался 
    # ведь у объекта типа RubyClass нету аттрибута name, у объекта типа RubyObject нету аттрибута name, у объе...
    def read_symbol_name(self) -> str:
        if Types(self.read_bytes()) is Types.SYMBOL:
            return self.read_symbol().name  
        else:
            return self.read_symbol_ref().name
    
    # выглядит пиздец колхозно но вроде самый быстрый способ
    # вообще можно было бы сделать модели всех объектов руби у них прописать методы
    # dump и load и потом просто вызывать их у type_byte 
    # но была бы бабка дедом да яйца по резьбе не подошли 
    def parse(self) -> RubyTypes:
        type_byte = Types(self.read_bytes())
        if type_byte is Types.TRUE:
            return True
        if type_byte is Types.FALSE:
            return False
        if type_byte is Types.NIL:
            return None
        if type_byte is Types.FIXNUM:
            return self.read_fixnum()
        if type_byte is Types.SYMBOL:
            return self.read_symbol()
        if type_byte is Types.SYMBOLREF:
            return self.read_symbol_ref()
        if type_byte is Types.OBJECTREF:
            return self.read_object_ref()
        if type_byte is Types.IVAR:
            return self.read_ivar()
        if type_byte is Types.EXTENDED:
            return self.read_extended()
        if type_byte is Types.ARRAY:
            return self.read_array()
        if type_byte is Types.BIGNUM:
            return self.read_bignum()
        if type_byte is Types.CLASS:
            return self.read_class()
        if type_byte is Types.MODULE:
            return self.read_class()
        if type_byte is Types.MORC:
            return self.read_class()  # обратная совместимость
        if type_byte is Types.DATA:
            return self.read_data()
        if type_byte is Types.FLOAT:
            return self.read_float()
        if type_byte is Types.HASH:
            return self.read_hash()
        if type_byte is Types.DEFAULTHASH:
            return self.read_hash_w_default_value()
        if type_byte is Types.OBJECT:
            return self.read_object()
        if type_byte is Types.REGEXP:
            return self.read_regexp()
        if type_byte is Types.STRING:
            return self.read_string()
        if type_byte is Types.STRUCT:
            return self.read_struct()
        if type_byte is Types.USERCLASS:
            return self.read_user_class()
        if type_byte is Types.USERDEFINED:
            return self.read_user_defined()
        if type_byte is Types.USERMARSHAL:
            return self.read_user_class()
            

def load(stream: BinaryIO) -> RubyTypes:
    return _Reader(stream).parse()


def load_from_file(filename: str) -> RubyTypes:
    with open(filename, 'rb') as f:
        return load(f)
    