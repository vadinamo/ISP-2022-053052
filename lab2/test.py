import os

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
        self.test_dict = {1: 'one'}
        self.test_value = 123
        self.test_bool = True

    def get_name(self):
        return self.test_str, self.test_list, self.test_dict, self.test_value, self.test_bool


def json_file_func_value_test() -> None:
    file_name = 'test.json'
    JsonSerializer.dump(f, file_name)
    func = JsonSerializer.load(file_name)
    os.remove(file_name)

    assert func(1) == f(1)


def toml_file_func_value_test() -> None:
    file_name = 'test.toml'
    TomlSerializer.dump(f, file_name)
    func = TomlSerializer.load(file_name)
    os.remove(file_name)

    assert func(1) == f(1)


def yaml_file_func_value_test() -> None:
    file_name = 'test.yaml'
    YamlSerializer.dump(f, file_name)
    func = YamlSerializer.load(file_name)
    os.remove(file_name)

    assert func(1) == f(1)


def json_string_func_value_test() -> None:
    json_string = JsonSerializer.dumps(f)
    func = JsonSerializer.loads(json_string)

    assert func(1) == f(1)


def toml_string_func_value_test() -> None:
    toml_string = TomlSerializer.dumps(f)
    func = TomlSerializer.loads(toml_string)

    assert func(1) == f(1)


def yaml_string_func_value_test() -> None:
    yaml_string = YamlSerializer.dumps(f)
    func = YamlSerializer.loads(yaml_string)

    assert func(1) == f(1)


def json_file_class_test() -> None:
    file_name = 'test.json'
    JsonSerializer.dump(TestClass, file_name)
    test_class = JsonSerializer.load(file_name)
    os.remove(file_name)

    assert test_class().get_name() == TestClass().get_name()


def toml_file_class_test() -> None:
    file_name = 'test.toml'
    TomlSerializer.dump(TestClass, file_name)
    test_class = TomlSerializer.load(file_name)
    os.remove(file_name)

    assert test_class().get_name() == TestClass().get_name()


def yaml_file_class_test() -> None:
    file_name = 'test.yaml'
    YamlSerializer.dump(TestClass, file_name)
    test_class = YamlSerializer.load(file_name)
    os.remove(file_name)

    assert test_class().get_name() == TestClass().get_name()


json_file_func_value_test()
toml_file_func_value_test()
yaml_file_func_value_test()

json_string_func_value_test()
toml_string_func_value_test()
yaml_string_func_value_test()

json_file_class_test()
toml_file_class_test()
yaml_file_class_test()
