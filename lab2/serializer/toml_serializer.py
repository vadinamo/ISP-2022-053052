from serializer.serializer import Serializer
import toml


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
            f.write(toml.dump(dictionary, f))
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
        return toml.dumps(dictionary)

    @staticmethod
    def load(fp: str):
        """
        Десериализует Python объект из файла формата toml

        :param fp: str
        :return: obj
        """
        with open(fp, "r") as f:
            dictionary = toml.load(f)
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
        dictionary = dict(toml.loads(s))
        dictionary = TomlSerializer.none_returning(dictionary)
        return Serializer.object_deserialization(dictionary)

    @staticmethod
    def none_removing(dictionary: dict) -> dict:
        """
        Меняет все None в словаре на строку __None__

        :param dictionary: dict
        :return: dict
        """
        for key, value in dictionary.items():
            if type(value) == dict:
                TomlSerializer.none_removing(value)

            elif type(value) == list:
                for i in range(len(value)):
                    if value[i] is None:
                        dictionary[key][i] = "__None__"

            elif value is None:
                dictionary[key] = "__None__"

            elif key is None:
                buffer = dictionary.pop(key)
                dictionary["__None__"] = buffer

        return dictionary

    @staticmethod
    def none_returning(dictionary: dict) -> dict:
        """
        Меняет все строки __None__ на None

        :param dictionary: dict
        :return: dict
        """
        for key, value in dictionary.items():
            if type(value) == dict:
                dictionary[key] = TomlSerializer.none_returning(value)

            elif type(value) == list:
                for i in range(len(value)):
                    if value[i] == "__None__":
                        dictionary[key][i] = None

            elif value == "__None__":
                dictionary[key] = None

            elif key == "__None__":
                buffer = dictionary.pop(key)
                dictionary[None] = buffer

        return dictionary
