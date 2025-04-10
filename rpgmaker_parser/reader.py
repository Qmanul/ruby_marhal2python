from marshal_dumper import reader
from marshal_dumper.reader import load, load_from_file

from rpgmaker_parser.models import RPGMAKER_USER_DEFINED, RPGMAKER_CLASSES  

# monkeypatching наше всё
for class_name, klass in RPGMAKER_USER_DEFINED.items():
    reader.register_user_defined_loader(class_name, klass.load)

for class_name, klass in RPGMAKER_CLASSES.items():      
    reader.register_object_loader(class_name, klass.load) 


_ = load, load_from_file  # чтобы ide не удалял импорт
 