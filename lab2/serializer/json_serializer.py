from serializer.serializer import Serializer
import inspect
from typing import *


class JsonSerializer(Serializer):
    @staticmethod
    def dump(obj, fp: str) -> None:
        """
        Сериализует Python объект в файл формата json

        :param obj:
        :param fp: str
        :return: None
        """
        json = JsonSerializer.dumps(obj)
        file = open(fp, 'w')
        file.write(json + '\n')
        file.close()

    @staticmethod
    def dumps(obj: object) -> str:
        """
        Сериализует Python объект в строку формата json

        :param obj:
        :return: str
        """
        dictionary = {}
        if inspect.isfunction(obj):
            dictionary = JsonSerializer.function_to_dictionary(obj)
        elif inspect.isclass(obj):
            dictionary = JsonSerializer.class_to_dictionary(obj)
        json = JsonSerializer.dictionary_to_json(dictionary)
        return json

    @staticmethod
    def load(fp: str) -> object:
        """
        Десериализует Python объект из файла формата json

        :param fp: str
        :return: obj
        """
        file = open(fp, 'r')
        json = ''
        for line in file:
            json += line
        file.close()
        return JsonSerializer.loads(json)

    @staticmethod
    def loads(s: str) -> object:
        """
        Десериализует Python объект из строки формата toml

        :param s: str
        :return: obj
        """
        dictionary = JsonSerializer.json_to_dictionary(s)
        obj = None
        obj = JsonSerializer.object_deserialization(dict(s))
        return obj

    @staticmethod
    def dictionary_to_json(dictionary: dict, level=1) -> str:
        """
        Converts dictionary to json format string.

        :param dictionary:
        :param level:
        :return:
        """
        json = '{\n'
        count = 0
        for key, value in dictionary.items():
            json += '\t' * level + JsonSerializer.value_to_json(key) + ': '
            if isinstance(value, dict):
                json += JsonSerializer.dictionary_to_json(value, level + 1)
            elif isinstance(value, (list, tuple, set, frozenset)):
                json += JsonSerializer.list_to_json(value, level + 1)
            else:
                json += JsonSerializer.value_to_json(value)
            json += '\n' if count == len(dictionary) - 1 else ',\n'
            count += 1
        json += '\t' * (level - 1) + '}'
        return json

    @staticmethod
    def list_to_json(_list: list, level: int) -> str:
        """Converts list to json format string."""
        json = '[\n'
        for i in range(len(_list)):
            json += '\t' * level + JsonSerializer.value_to_json(_list[i], level + 1) + ('\n' if i == len(_list) - 1 else ',\n')
        json += '\t' * (level - 1) + ']'
        return json

    @staticmethod
    def json_to_dictionary(json: str) -> Dict[Any, Any]:
        """Converts json format string to dictionary."""
        dictionary = {}
        key = ''
        value = ''
        key_writing = False
        value_writing = False
        close = ''
        close_setting = False
        count = 0
        for i in range(len(json)):
            if json[i] == '"' and not value_writing and not close_setting:
                if not key_writing:
                    key_writing = True
                    continue
                else:
                    key_writing = False
                    continue
            if json[i] == ' ' and not key_writing and not value_writing:
                close_setting = True
                continue
            if close_setting:
                close_setting = False
                if json[i] == '"':
                    close = '"'
                    count -= 1
                elif json[i] == '[':
                    close = ']'
                elif json[i] == '{':
                    close = '}'
                else:
                    close = '\n'
                    count -= 1
                    value += json[i]
                value_writing = True
                continue
            if key_writing:
                key += json[i]
            if value_writing:
                if (close == '}' and json[i] == '{') or (close == ']' and json[i] == '[') or \
                        (close == ')' and json[i] == '('):
                    count += 1
                if (close == '}' and json[i] == '}') or (close == ']' and json[i] == ']') or \
                        (close == ')' and json[i] == ')'):
                    count -= 1
                if (json[i] == close and count == -1) or (close == '\n' and (json[i] == ',' or json[i] == '\n')):
                    value_writing = False
                    if json[i] == '"':
                        dictionary[key] = JsonSerializer.json_to_value(value)
                    elif json[i] == ']':
                        dictionary[key] = JsonSerializer.json_to_list(value)
                    elif json[i] == '}':
                        dictionary[key] = JsonSerializer.json_to_dictionary(value)
                    else:
                        dictionary[key] = JsonSerializer.json_to_value(value)
                    key = ''
                    value = ''
                    close = ''
                    count = 0
                else:
                    value += json[i]
        return dictionary

    @staticmethod
    def json_to_list(json: str) -> List[Any]:
        """Converts json format string to list."""
        _list = []
        value = ''
        value_writing = False
        close = ''
        count = 0
        for i in range(len(json) - 1):
            if json[i] == '\t' and not json[i + 1] == '\t' and not value_writing:
                value_writing = True
                if json[i + 1] == '{':
                    close = '}'
                if json[i + 1] == '[':
                    close = ']'
                continue
            if close == '}' or close == ']':
                if (close == '}' and json[i] == '{') or (close == ']' and json[i] == '[') or \
                        (close == ')' and json[i] == '('):
                    count += 1
                if (close == '}' and json[i] == '}') or (close == ']' and json[i] == ']') or \
                        (close == ')' and json[i] == ')'):
                    count -= 1
                if json[i] == close and count == 0:
                    value_writing = False
                    if json[i] == ']':
                        _list.append(JsonSerializer.json_to_list(value))
                    elif json[i] == '}':
                        _list.append(JsonSerializer.json_to_dictionary(value))
                    value = ''
                    close = ''
            else:
                if (json[i] == ',' and json[i + 1] == '\n') or json[i] == '\n':
                    value_writing = False
                    if not value == '':
                        _list.append(JsonSerializer.json_to_value(value))
                    value = ''
            if value_writing:
                value += json[i]
        return _list

    @staticmethod
    def json_to_value(json: str) -> Any:
        """Converts json format string to value."""
        if json.isdigit() or (json[0] == '-' and json.replace('-', '').isdigit()):
            return int(json)
        if '.' in json:
            temp = json.replace('.', '', 1)
            temp = JsonSerializer.json_to_value(temp)
            if isinstance(temp, int):
                return float(json)
        if json == 'true':
            return True
        if json == 'false':
            return False
        if json == 'null':
            return None
        if json[0] == '"':
            return json[1:-1]
        return json

    @staticmethod
    def value_to_json(value: Any, level=0) -> str:
        """Converts value to json format string."""
        if isinstance(value, str):
            return '"' + value + '"'

        if isinstance(value, bool):
            return str(value).lower()

        if isinstance(value, (int, float)):
            return str(value)

        if isinstance(value, dict):
            return JsonSerializer.dictionary_to_json(value, level)

        if isinstance(value, list):
            return JsonSerializer.list_to_json(value, level)

        return 'null'
