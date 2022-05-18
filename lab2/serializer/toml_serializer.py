from serializer.serializer import Serializer
import tomli
import tomli_w


class TomlSerializer(Serializer):
    """
    Данный класс позволяет сериализовать объекты в формат toml и десериализовать обратно
    """

    @staticmethod
    def dump(obj, fp: str) -> None:
        """
        Сериализует Python объект в файл формата toml

        :param obj:
        :param fp: str
        :return: None
        """
        dictionary = Serializer.object_serialization(obj)
        dictionary = TomlSerializer.none_removing(dictionary)

        with open(fp, 'w') as f:
            f.write(tomli_w.dumps(dictionary))
            f.close()

    @staticmethod
    def dumps(obj) -> str:
        """
        Сериализует Python объект в строку формата toml

        :param obj:
        :return: str
        """
        dictionary = Serializer.object_serialization(obj)
        dictionary = TomlSerializer.none_removing(dictionary)
        return tomli_w.dumps(dictionary)

    @staticmethod
    def load(fp: str):
        """
        Десериализует Python объект из файла формата toml

        :param fp: str
        :return: obj
        """
        with open(fp, 'rb') as f:
            dictionary = tomli.load(f)
            f.close()

        dictionary = TomlSerializer.none_returning(dict(dictionary))

        return Serializer.object_deserialization(dictionary)

    @staticmethod
    def loads(s: str):
        """
        Десериализует Python объект из строки формата toml

        :param s: str
        :return: obj
        """
        dictionary = dict(tomli.loads(s))
        dictionary = TomlSerializer.none_returning(dictionary)

        return Serializer.object_deserialization(dictionary)

    @staticmethod
    def none_removing(dictionary: dict) -> dict:
        """
        Меняет все типы None в словаре на строку "None"

        :param dictionary: dict
        :return: dict
        """
        for key, value in dictionary.items():
            if type(value) == dict:
                TomlSerializer.none_removing(value)

            elif type(value) == list:
                for i in range(len(value)):
                    if value[i] is None:
                        dictionary[key][i] = 'None'

            elif value is None:
                dictionary[key] = 'None'

            elif key is None:
                buffer = dictionary.pop(key)
                dictionary['None'] = buffer

            if key == 'co_consts':
                value = list(value)
                for i in range(len(value)):
                    if value[i] is None:
                        value[i] = 'None'

                dictionary[key] = Serializer.list_to_tuple(value)
        return dictionary

    @staticmethod
    def none_returning(dictionary: dict) -> dict:
        """
        Меняет все строки "None" на тип None

        :param dictionary: dict
        :return: dict
        """
        for key, value in dictionary.items():
            if isinstance(value, dict):
                dictionary[key] = TomlSerializer.none_returning(value)

            elif type(value) == list:
                for i in range(len(value)):
                    if value[i] == 'None':
                        dictionary[key][i] = None

            elif value == 'None':
                dictionary[key] = None

            elif key == 'None':
                buffer = dictionary.pop(key)
                dictionary[None] = buffer

        return dictionary
