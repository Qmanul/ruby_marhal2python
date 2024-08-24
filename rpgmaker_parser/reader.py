import struct

from marshal_dumper.reader import register_user_defined, load, register_user_class

from rpgmaker_parser.models import RPGEventCommand, Table, Tone, RPGMAKER_CLASSES

_ = load


def read_table(data: bytes):
    zsize, xsize, ysize, zsize, size = struct.unpack('<5L', data[:20])
    
    if zsize * xsize * ysize != size:
        raise ValueError(f'Unexpected size {zsize * xsize * ysize} != {size}')
    
    # не правильный результат т.к. байты идут от младшего к старшему
    dataview = memoryview(data[20:]).cast("H", (zsize, ysize, xsize))  # type: ignore
    return Table(dataview.tolist())
    
register_user_defined('Table', read_table)
register_user_defined('Tone', lambda data: Tone(*(struct.unpack('<4d', data))))

for class_name, class_ in RPGMAKER_CLASSES.items():        
    register_user_class(class_name, class_) 

    