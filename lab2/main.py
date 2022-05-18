from serializer.json_serializer import JsonSerializer
from serializer.toml_serializer import TomlSerializer
from serializer.yaml_serializer import YamlSerializer
import math
c = 42


def f(x):
    a = 123
    return math.sin(x * a * c)


class TestClass:
    def __init__(self):
        self.test_str = 'test success'
        self.test_list = [1, 2]
        self.test_value = 123
        self.test_bool = True
        self.test_dict = {1: "1"}

    def get_name(self):
        return self.test_str, self.test_list, self.test_value, self.test_bool, self.test_dict


def t():
    def a():
        print(c)

    return a


def main():
    file_name = 'test1'

    YamlSerializer.dump(f, file_name)
    func = YamlSerializer.load(file_name)
    print(func(1))

    TomlSerializer.dump(func, file_name)
    func = TomlSerializer.load(file_name)
    print(func(1))

    JsonSerializer.dump(func, file_name)
    func = JsonSerializer.load(file_name)
    print(func(1))

    file_name = 'test2'

    YamlSerializer.dump(TestClass, file_name)
    test_class = YamlSerializer.load(file_name)
    print(test_class().get_name())

    TomlSerializer.dump(test_class, file_name)
    test_class = TomlSerializer.load(file_name)
    print(test_class().get_name())

    JsonSerializer.dump(test_class, file_name)
    test_class = JsonSerializer.load(file_name)
    print(test_class().get_name())


if __name__ == '__main__':
    main()
