from serializer.json_serializer import JsonSerializer
from serializer.toml_serializer import TomlSerializer
from serializer.yaml_serializer import YamlSerializer
import math
c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


class Aboba:
    def __init__(self):
        self.name = 'aboba'

    def get_name(self):
        print(self.name)


def main():
    file_name = 'test1'
    YamlSerializer.dump(Aboba, file_name)
    a = YamlSerializer.load(file_name)
    print(a(1))

    file_name = 'test2'
    TomlSerializer.dump(f, file_name)


    # b = toml.object_serialization(Aboba)
    # cls = Serializer.object_deserialization(b)
    # obj = cls()
    # obj.get_name()


if __name__ == '__main__':
    main()
