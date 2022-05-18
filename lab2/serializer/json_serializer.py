from serializer.serializer import Serializer
from typing import Any


class JsonSerializer(Serializer):
    @staticmethod
    def dump(obj: object, fp: str) -> None:
        """
        Сериализует Python объект в файл формата json

        :param obj:
        :param fp: str
        :return: None
        """
        s = JsonSerializer.dumps(obj)
        file = open(fp, 'w')
        file.write(s + '\n')
        file.close()

    @staticmethod
    def dumps(obj: object) -> str:
        """
        Сериализует Python объект в строку формата json

        :param obj:
        :return: str
        """
        dictionary = JsonSerializer.object_serialization(obj)
        s = JsonSerializer.dictionary_to_json(dictionary)
        return s

    @staticmethod
    def load(fp: str) -> Any:
        """
        Десериализует Python объект из файла формата json

        :param fp: str
        :return: Any
        """
        file = open(fp, 'r')
        s = ''
        for line in file:
            s += line
        file.close()
        return JsonSerializer.loads(s)

    @staticmethod
    def loads(s: str) -> Any:
        """
        Десериализует Python объект из строки формата json

        :param s: str
        :return: Any
        """
        dictionary = JsonSerializer.json_to_dictionary(s)
        obj = JsonSerializer.object_deserialization(dictionary)
        return obj

    @staticmethod
    def dictionary_to_json(dictionary: dict, tabs=1) -> str:
        """
        Конвертирует словарь в json

        :param dictionary: dict
        :param tabs:
        :return:
        """
        s = '{\n'
        count = 0
        for key, value in dictionary.items():
            s += '\t' * tabs + JsonSerializer.instance_to_json(key) + ': '
            if isinstance(value, dict):
                s += JsonSerializer.dictionary_to_json(value, tabs + 1)

            elif isinstance(value, (list, tuple, set, frozenset, bytes)):
                s += JsonSerializer.list_to_json(value, tabs + 1)

            else:
                s += JsonSerializer.instance_to_json(value)

            s += '\n' if count == len(dictionary) - 1 else ',\n'
            count += 1
        s += '\t' * (tabs - 1) + '}'

        return s

    @staticmethod
    def list_to_json(_list: list, tabs: int) -> str:
        """
        Конвертирует list в строку формата json

        :param _list: list
        :param tabs: int
        :return:
        """
        s = '[\n'
        for i in range(len(_list)):
            s += '\t' * tabs + JsonSerializer.instance_to_json(_list[i], tabs + 1) + ('\n' if i == len(_list) - 1
                                                                                     else ',\n')
        s += '\t' * (tabs - 1) + ']'

        return s

    @staticmethod
    def json_to_dictionary(s: str) -> dict:
        """
        Конвертирует формат json в словарь

        :param s: str
        :return: dict
        """
        dictionary = {}
        key = ''
        value = ''
        close = ''

        key_writing = False
        value_writing = False
        close_setting = False

        count = 0

        for i in range(len(s)):
            if s[i] == '"' and not value_writing and not close_setting:
                if not key_writing:
                    key_writing = True
                    continue

                else:
                    key_writing = False
                    continue

            if s[i] == ' ' and not key_writing and not value_writing:
                close_setting = True
                continue

            if close_setting:
                close_setting = False
                if s[i] == '"':
                    close = '"'
                    count -= 1

                elif s[i] == '[':
                    close = ']'

                elif s[i] == '{':
                    close = '}'

                else:
                    close = '\n'
                    count -= 1
                    value += s[i]
                value_writing = True
                continue

            if key_writing:
                key += s[i]

            if value_writing:
                if (close == '}' and s[i] == '{') \
                        or (close == ']' and s[i] == '[') \
                        or (close == ')' and s[i] == '('):
                    count += 1

                if (close == '}' and s[i] == '}') \
                        or (close == ']' and s[i] == ']') \
                        or (close == ')' and s[i] == ')'):
                    count -= 1

                if (s[i] == close and count == -1) or (close == '\n' and (s[i] == ',' or s[i] == '\n')):
                    value_writing = False
                    if s[i] == '"':
                        dictionary[key] = JsonSerializer.json_to_value(value)

                    elif s[i] == ']':
                        dictionary[key] = JsonSerializer.json_to_list(value)

                    elif s[i] == '}':
                        dictionary[key] = JsonSerializer.json_to_dictionary(value)

                    else:
                        dictionary[key] = JsonSerializer.json_to_value(value)

                    key = ''
                    value = ''
                    close = ''
                    count = 0

                else:
                    value += s[i]

        return dictionary

    @staticmethod
    def json_to_list(s: str) -> list:
        """
        Конвертирует строку формата json в list

        :param s: str
        :return: list
        """
        _list = []
        value = ''
        value_writing = False
        close = ''
        count = 0
        for i in range(len(s) - 1):
            if s[i] == '\t' and not s[i + 1] == '\t' and not value_writing:
                value_writing = True

                if s[i + 1] == '{':
                    close = '}'

                if s[i + 1] == '[':
                    close = ']'

                continue

            if close == '}' or close == ']':
                if (close == '}' and s[i] == '{') \
                        or (close == ']' and s[i] == '[') \
                        or (close == ')' and s[i] == '('):
                    count += 1

                if (close == '}' and s[i] == '}') \
                        or (close == ']' and s[i] == ']') \
                        or (close == ')' and s[i] == ')'):
                    count -= 1

                if s[i] == close and count == 0:
                    value_writing = False
                    if s[i] == ']':
                        _list.append(JsonSerializer.json_to_list(value))

                    elif s[i] == '}':
                        _list.append(JsonSerializer.json_to_dictionary(value))

                    value = ''
                    close = ''
            else:
                if (s[i] == ',' and s[i + 1] == '\n') or s[i] == '\n':
                    value_writing = False
                    if not value == '':
                        _list.append(JsonSerializer.json_to_value(value))
                    value = ''

            if value_writing:
                value += s[i]

        return _list

    @staticmethod
    def json_to_value(s: str):
        """
        Конвертирует строку формата json в значение

        :param s: str
        """
        if s.isdigit() or (s[0] == '-' and s.replace('-', '').isdigit()):
            return int(s)

        if '.' in s:
            temp = s.replace('.', '', 1)
            temp = JsonSerializer.json_to_value(temp)
            if isinstance(temp, int):
                return float(s)

        if s == 'true':
            return True

        if s == 'false':
            return False

        if s == 'null':
            return None

        if s[0] == '"':
            return s[1:-1]

        return s

    @staticmethod
    def instance_to_json(value: Any, tabs=0) -> str:
        """
        Конвертирует значение в строку формата json

        :param value: Any
        :param tabs: int
        :return: str
        """
        if isinstance(value, str):
            return '"' + value + '"'

        if isinstance(value, bool):
            return str(value).lower()

        if isinstance(value, (int, float)):
            return str(value)

        if isinstance(value, dict):
            return JsonSerializer.dictionary_to_json(value, tabs)

        if isinstance(value, list):
            return JsonSerializer.list_to_json(value, tabs)

        else:
            return 'null'
