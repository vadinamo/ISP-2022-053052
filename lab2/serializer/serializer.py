import importlib
import inspect
import struct
from abc import abstractmethod, ABC
from types import CodeType, FunctionType


class Serializer(ABC):
    """
    Класс позволяет конвертировать объекты в словари и словари обратно в объекты
    """

    @staticmethod
    @abstractmethod
    def dump(obj, fp: str) -> None:
        """
        Сериализует Python объект в файл
        """
        pass

    @staticmethod
    @abstractmethod
    def dumps(obj) -> str:
        """
        Сериализует Python объект в строку
        """
        pass

    @staticmethod
    @abstractmethod
    def load(fp: str):
        """
        Десериализует Python объект из файла
        """
        pass

    @staticmethod
    @abstractmethod
    def loads(s: str):
        """
        Десериализует Python объект из строки
        """
        pass

    @staticmethod
    def object_serialization(obj) -> dict:
        """
        Принимает объект и конвертирует его в словарь

        :param obj:
        :return: dict
        """
        if inspect.isfunction(obj):
            return Serializer.function_to_dictionary(obj)

        if inspect.isclass(obj):
            return Serializer.class_to_dictionary(obj)

    @staticmethod
    def object_deserialization(dictionary):
        """
        Конвертирует словарь в объект

        :param dictionary: dict
        :return: object
        """
        if isinstance(dictionary, dict):
            for key in dictionary.keys():
                if key == "__code__":
                    return Serializer.dictionary_to_function(dictionary)
                if key == "__init__":
                    return Serializer.dictionary_to_class(dictionary)

    @staticmethod
    def get_function_attributes() -> dict:
        """
        Возвращает словрь атрибутов функции со значениями по умолчанию

        :return: dict
        """
        return {'co_argcount': None,
                'co_posonlyargcount': None,
                'co_kwonlyargcount': None,
                'co_nlocals': None,
                'co_stacksize': None,
                'co_flags': None,
                'co_code': None,
                'co_consts': (),
                'co_names': (),
                'co_varnames': (),
                'co_filename': None,
                'co_name': None,
                'co_firstlineno': None,
                'co_lnotab': None,
                'co_freevars': (),
                'co_cellvars': ()}

    @staticmethod
    def function_to_dictionary(_function: FunctionType) -> dict:
        """
        Конвертирует функцию в словарь

        :param _function: FunctionType
        :return: dict
        """
        _globals = {}
        co_names = _function.__code__.co_names
        global_attributes = _function.__globals__

        for key, value in global_attributes.items():
            if key in co_names or key in _function.__code__.co_consts:
                if inspect.ismodule(value):
                    _globals[key] = 'module'
                else:
                    _globals[key] = value

        _code = Serializer.code_to_dictionary(_function.__code__)

        return {'__name__': _function.__name__,
                '__code__': _code,
                '__defaults__': _function.__defaults__,
                '__globals__': _globals}

    @staticmethod
    def list_to_tuple(_list: list) -> tuple:
        """
        Конвертирует список в кортеж

        :param _list: list
        :return: tuple
        """
        if not isinstance(_list, type(None)):
            for i in range(len(_list)):
                if isinstance(_list[i], list):
                    _list[i] = Serializer.list_to_tuple(_list[i])

            return tuple(_list)

        else:
            return ()

    @staticmethod
    def code_to_dictionary(_code: CodeType) -> dict:
        """
        Конвертирует код в словарь

        :param _code: CodeType
        :return: dict
        """
        code_dict = {}
        code_attributes = dict(inspect.getmembers(_code))

        for key, value in code_attributes.items():
            if key in Serializer.get_function_attributes().keys():
                if key == 'co_consts':
                    value = list(value)
                    for i in range(len(value)):
                        if inspect.iscode(value[i]):
                            value[i] = Serializer.code_to_dictionary(value[i])

                    value = Serializer.list_to_tuple(value)
                code_dict[key] = value
                if key == 'co_code' or key == 'co_lnotab':
                    code_dict[key] = Serializer.bytes_to_tuple(value)
        return code_dict

    @staticmethod
    def dictionary_to_code(function_attributes: dict) -> CodeType:
        """
        Конвертирует словарь в код

        :param function_attributes: dict
        :return: CodeType
        """
        for key, value in function_attributes.items():
            if key == 'co_consts':
                consts = list(value)
                for i in range(len(consts)):
                    if isinstance(consts[i], dict):
                        consts[i] = Serializer.dictionary_to_code(consts[i])

                value = Serializer.list_to_tuple(consts)
                function_attributes[key] = value

        attributes_list = []
        for attribute in Serializer.get_function_attributes():
            attributes_list.append(function_attributes[attribute])

        if isinstance(attributes_list[6], tuple):
            attributes_list[6] = bytes(attributes_list[6])

        if isinstance(attributes_list[13], tuple):
            attributes_list[13] = bytes(attributes_list[13])

        return CodeType(*attributes_list)

    @staticmethod
    def dictionary_to_function(function_dictionary: dict) -> FunctionType:
        """
        Конвертирует словарь в функцию

        :param function_dictionary: dict
        :return: FunctionType
        """
        function_attributes = Serializer.get_function_attributes()

        for key, value in function_dictionary['__code__'].items():
            if isinstance(value, list):
                value = Serializer.list_to_tuple(value)
            if key in function_attributes.keys():
                function_attributes[key] = value

        for key, value in function_dictionary['__globals__'].items():
            if value == 'module':
                function_dictionary['__globals__'][key] = importlib.import_module(key)

        function_dictionary['__globals__']['__builtins__'] = __builtins__

        if isinstance(function_dictionary['__defaults__'], list):
            _globals = Serializer.list_to_tuple(function_dictionary['__defaults__'])

        else:
            _globals = function_dictionary['__defaults__']

        return FunctionType(Serializer.dictionary_to_code(function_attributes),
                            function_dictionary['__globals__'],
                            function_dictionary['__name__'],
                            _globals)

    @staticmethod
    def class_to_dictionary(_class: type) -> dict:
        """
        Конвертирует класс в словарь

        :param _class: class
        :return: dict
        """
        class_dict = {}
        attribute_class = inspect.getmembers(_class)

        for key, value in attribute_class:
            if key[0] != "_":
                if inspect.ismethod(value):
                    class_dict[key] = Serializer.function_to_dictionary(value.__func__)

                elif isinstance(value, (int, float, bool, str, bytes,
                                        list, set, frozenset, tuple, dict)):
                    class_dict[key] = value

                elif inspect.isfunction(value):
                    class_dict[key] = Serializer.function_to_dictionary(value)

                elif inspect.isclass(value):
                    class_dict[key] = Serializer.class_to_dictionary(value)

            elif key == "__init__":
                class_dict[key] = Serializer.function_to_dictionary(value)

        return class_dict

    @staticmethod
    def dictionary_to_class(class_dictionary: dict) -> type:
        """
        Конвертирует словарь в класс

        :param class_dictionary: dict
        :return: class
        """
        for key, value in class_dictionary.items():
            if isinstance(value, dict):
                for master_key in value.keys():

                    if master_key == '__init__':
                        class_dictionary['__globals__'][key] = Serializer.dictionary_to_class(value)

                    if master_key == '__code__':
                        class_dictionary[key] = Serializer.dictionary_to_function(value)

        instance = type("class", (), class_dictionary)

        return instance

    @staticmethod
    def bytes_to_tuple(x: bytes) -> tuple:
        """
        Конвертирует bytes в tuple
        :param x: bytes
        :return: tuple
        """
        data_ints = struct.unpack('<' + 'B' * len(x), x)
        return data_ints
