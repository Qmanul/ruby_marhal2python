from __future__ import annotations

import re
from typing import BinaryIO, NoReturn
from collections import defaultdict

from models import RubyClass, RubySymbol, RubyObject, RubyTypes
from exception import VersionError, TypeNotSupportedError
from constants import Types, MARSHAL_MAJOR_VERSION, MARSHAL_MINOR_VERSION

class Reader:
    __slots__ = '_stream', '_symbols', '_objects', '_byte_read_map' 
    def __init__(self, stream: BinaryIO) -> None:
        self._stream = stream
        self._check_marshal_version()
        self._objects: list[RubyTypes] = []
        self._symbols: list[RubySymbol] = []  # почему у символов отдельная таблица ??? 
      
    def _check_marshal_version(self) -> None | NoReturn:  # я тут выёбывыаюсь знанием типов (посмотрел 1 видео)
        major_version = ord(self._read_bytes())
        minor_version = ord(self._read_bytes())
        if major_version != MARSHAL_MAJOR_VERSION or minor_version > MARSHAL_MINOR_VERSION:
            raise VersionError(f'{MARSHAL_MAJOR_VERSION}.{MARSHAL_MINOR_VERSION}',
                               f'{major_version}.{minor_version}')
        return None  # mypy зачем? почему? по кочану!

    # метод шобы не писать self._stream.read(ln)
    def _read_bytes(self, ln: int = 1) -> bytes:
        return self._stream.read(ln)

    def _read_symbol(self) -> RubySymbol:
        self._symbols.append(RubySymbol(name=self._read_bytes(self._read_fixnum()).decode()))
        return self._symbols[-1]

    def _read_symbol_ref(self) -> RubySymbol:
        return self._symbols[self._read_fixnum()]

    def _read_fixnum(self) -> int:
        ln = ord(self._read_bytes())
        if 6 <= ln <= 127:
            return ln - 5
        if 128 <= ln <= 250:
            return ln - 251  # ???? кто это нахуй придумал???? почему 251???? а блять потому что 256 - 5 ну ахуеть

        res = 0
        const = 0 if ln <= 4 else 256  # понятия не имею как назвать переменную пусть буит const
        for exp in range(abs(const - ln)):
            res += (ord(self._read_bytes()) - const) * 256 ** exp
        return res

    def _read_object_ref(self) -> RubyTypes:
        return self._objects[self._read_fixnum() - 1]  # почему индекс объектов начинается с 1, тогда как символов с 0 ???

    def _read_regexp(self) -> re.Pattern:
        pattern = self._read_bytes(self._read_fixnum()).decode('US-ASCII')
        flags = ord(self._read_bytes())
        options = sum(re_flag for flag, re_flag in {1: re.I, 2: re.X, 4: re.S}.items() if flags & flag)  # спасибо tabnine
        res = re.compile(pattern, options)
        self._objects.append(res)
        return res

    def _read_string(self) -> str:
        s = self._read_bytes(self._read_fixnum()).decode('UTF-8')
        self._objects.append(s)
        return s

    # ну и залупа кто это придумал
    def _read_ivar(self) -> RubyTypes:
        type_byte = Types(self._read_bytes())
        if type_byte is Types.STRING:  # модно сделать match case но python < 3.10
            s = self._read_bytes(self._read_fixnum())
        elif type_byte is Types.REGEXP:
            s = self._read_bytes(self._read_fixnum())
            flags = ord(self._read_bytes())
            options = sum(re_flag for flag, re_flag in {1: re.I, 2: re.X, 4: re.S}.items() if flags & flag)
        elif type_byte in (Types.USERDEFINED, Types.USERCLASS): 
            o = self._read_user_defined() if type_byte is Types.USERDEFINED else self._read_user_class()
            # mypy пожалуйста
            o.set_attributes(self._read_attributes())  # type: ignore
            self._objects.append(o)
            return o
        else:
            raise TypeNotSupportedError(type_byte.name)
               
        attrs = self._read_attributes()
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
            res = re.compile(res, options)  # type: ignore
        self._objects.append(res)
        return res

    def _read_extended(self):
        self._read_symbol()  # нам особо нет дела до имени модуля
        return self.parse()

    def _read_array(self) -> list:
        a = [self.parse() for _ in range(self._read_fixnum())]
        self._objects.append(a)
        return a

    def _read_bignum(self) -> int:
        sign = self._read_bytes().decode()  # '+' | '-'
        data = self._read_bytes(self._read_fixnum() * 2)  # зачем надо было делить длину на 2 :FaunaTired:
        # https://ruby-doc.org/3.2.2/marshal_rdoc.html#label-Bignum
        res = 0
        for exp, byte in enumerate(data):
            res |= byte << (exp * 8)  # спасибо tabnine
        if sign == '-':
            res = -res
        self._objects.append(res)
        return res

    def _read_class(self) -> RubyClass:
        c = RubyClass(name=self._read_bytes(self._read_fixnum()).decode())
        self._objects.append(c)  # Да. Я пихаю класс к объектам. Это питон детка!
        return c
    
    def _read_module(self):
        return self._read_class()  # они читаются одинаково ацтань!

    # вроде можно дампить, но там как то хитровыебанно поэтому пока просто кидаем ошибку мб когда-нибудь сделаю
    def _read_data(self):
        raise TypeNotSupportedError('Data')

    def _read_float(self) -> float:
        f = float(self._read_bytes(self._read_fixnum()))  # 0.0, NaN, inf, -inf
        self._objects.append(f) 
        return f

    def _read_hash(self) -> dict:
        h = {self.parse(): self.parse() for _ in range(self._read_fixnum())}
        self._objects.append(h)
        return h

    # почему ты есть
    def _read_hash_w_default_value(self) -> dict:
        # Сначала читаем хеш потому что дефолт валью в конце. Очень удобно спасибо руби
        h = self._read_hash()
        # я так счастлив я так рад у меня есть дефолтдикт, хочу сказать благодарю и говорю "соси"
        # соси благодраю тебя, соси спасибо, что ты есть
        # ну а не серьёзной ноте, я хз если это работает с объектами
        h = defaultdict(lambda: self.parse(), h)
        self._objects.append(h)
        return h

    def _read_object(self) -> RubyObject:
        o = RubyObject(cls_name=self._read_name_symbol(), attributes=self._read_attributes())
        self._objects.append(o)
        return o

    def _read_struct(self) -> RubyObject:
        o = RubyObject(cls_name=self._read_name_symbol()[8:], attributes=self._read_attributes())  # [8:] отсекает 'Struct::'
        self._objects.append(o)
        return o

    # 3 метода ниже это ёбанное богохульство я не буду их имплементить
    # upd: ладно хуй с ним
    def _read_user_defined(self) -> RubyObject:
        o = RubyObject(cls_name=self._read_name_symbol(), attributes={"data":self._read_bytes(self._read_fixnum())})
        self._objects.append(o)
        return o
        
    def _read_user_class(self) -> RubyObject:
        o = RubyObject(cls_name=self._read_name_symbol(), attributes={'data': self.parse()}) 
        self._objects.append(o)
        return o
    
    def _read_user_marshal(self) -> RubyObject:
        return self._read_user_class()  # они тоже читаются одинаково ацтань!
    
    def _read_attributes(self) -> dict:
        return {self._read_name_symbol(): self.parse() for _ in range(self._read_fixnum())}
    
    # метод штобы mypy не ругался 
    # ведь у объекта типа RubyClass нету проперти name, у объекта типа RubyObject нету проперти name, у объе...
    def _read_name_symbol(self) -> str:
        return self._read_symbol().name if Types(self._read_bytes()) is Types.SYMBOL else self._read_symbol_ref().name
        
    def parse(self) -> RubyTypes:
        type_byte = Types(self._read_bytes())
        if type_byte is Types.TRUE:
            return True
        if type_byte is Types.FALSE:
            return False
        if type_byte is Types.NIL:
            return None
        if type_byte is Types.FIXNUM:
            return self._read_fixnum()
        if type_byte is Types.SYMBOL:
            return self._read_symbol()
        if type_byte is Types.SYMBOLREF:
            return self._read_symbol_ref()
        if type_byte is Types.OBJECTREF:
            return self._read_object_ref()
        if type_byte is Types.IVAR:
            return self._read_ivar()
        if type_byte is Types.EXTENDED:
            return self._read_extended()
        if type_byte is Types.ARRAY:
            return self._read_array()
        if type_byte is Types.BIGNUM:
            return self._read_bignum()
        if type_byte is Types.CLASS:
            return self._read_class()
        if type_byte is Types.MODULE:
            return self._read_module()
        if type_byte is Types.MORC:
            return self._read_class()  # обратная совместимость
        if type_byte is Types.DATA:
            return self._read_data()
        if type_byte is Types.FLOAT:
            return self._read_float()
        if type_byte is Types.HASH:
            return self._read_hash()
        if type_byte is Types.DEFAULTHASH:
            return self._read_hash_w_default_value()
        if type_byte is Types.OBJECT:
            return self._read_object()
        if type_byte is Types.REGEXP:
            return self._read_regexp()
        if type_byte is Types.STRING:
            return self._read_string()
        if type_byte is Types.STRUCT:
            return self._read_struct()
        if type_byte is Types.USERCLASS:
            return self._read_user_class()
        if type_byte is Types.USERDEFINED:
            return self._read_user_defined()
        if type_byte is Types.USERMARSHAL:
            return self._read_user_marshal()
            

def load(stream: BinaryIO) -> RubyTypes:
    return Reader(stream).parse()
