import dataclasses
from marshal_dumper import reader
import pprint
import struct

from marshal_dumper.models import RubyObject

old_reader = reader._Reader.read_user_defined 


@dataclasses.dataclass(frozen=True, slots=True)
class RubyTone:
    red: int
    green: int
    blue: int
    alpha_or_grey: int


@dataclasses.dataclass(frozen=True, slots=True)
class RubyTable:
    data: list[list[list[int]]]
    
    
def new_reader(self):
    obj_ = old_reader(self)
    match obj_:
        case RubyObject(cls_name='Table', attributes={'data': data}) if data:
            zsize, xsize, ysize, zsize, size = struct.unpack('<5L', data[:20])
            
            if zsize * xsize * ysize != size:
                raise ValueError(f'Unexpected size {zsize * xsize * ysize} != {size}')
            
            dataview = memoryview(data[20:]).cast('H', (zsize, ysize, xsize))
            obj_ = RubyTable(dataview.tolist())
                            
        case RubyObject(cls_name='Tone', attributes={'data': data}) if data:
            obj_ = RubyTone(*(struct.unpack('<4d', data)))
                 
    return obj_
    
    
def main() -> None:
    reader._Reader.read_user_defined = new_reader    
    
    with open(r'E:\PythonProjects\ruby_marhal2python\Map070.rxdata', 'rb') as input, open('out.txt', 'w+', encoding="utf-8") as output: 
        data = reader.load(input)
        pprint.pprint(data, output, )
    


if __name__ == '__main__':
    main()
