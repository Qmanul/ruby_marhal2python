from enum import Enum


MARSHAL_MAJOR_VERSION: int = 4
MARSHAL_MINOR_VERSION: int = 8

# просто энамчик типов байтов
class Types(Enum):
    TRUE = b'T'
    FALSE = b'F'
    NIL = b'0'
    FIXNUM = b'i'
    SYMBOL = b':'
    SYMBOLREF = b';'
    OBJECTREF = b'@'
    IVAR = b'I'
    EXTENDED = b'e'
    ARRAY = b'['
    BIGNUM = b'l'
    CLASS = b'c'
    MODULE = b'm'
    MORC = b'M'  # Module OR Class получается морс
    DATA = b'd'
    FLOAT = b'f'
    HASH = b'{'
    DEFAULTHASH = b'}'
    OBJECT = b'o'
    REGEXP = b'/'
    STRING = b'"'
    STRUCT = b'S'
    USERCLASS = b'C'
    USERDEFINED = b'u'
    USERMARSHAL = b'U'
