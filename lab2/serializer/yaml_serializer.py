from serializer.serializer import Serializer
from typing import Any
import yaml


class YamlSerializer(Serializer):
    """
    Данный класс позволяет сериализовать объекты в формат yaml и десериализовать обратно
    """

    @staticmethod
    def dump(obj: object, fp: str) -> None:
        """
        Сериализует Python объект в файл формата yaml

        :param obj: object
        :param fp: str
        :return: None
        """
        dictionary = Serializer.object_serialization(obj)
        with open(fp, 'w') as f:
            f.write(yaml.dump(dictionary))
            f.close()

    @staticmethod
    def dumps(obj: object) -> str:
        """
        Сериализует Python объект в строку формата yaml

        :param obj: object
        :return: str
        """
        dictionary = Serializer.object_serialization(obj)
        return yaml.dump(dictionary)

    @staticmethod
    def load(fp: str) -> Any:
        """
        Десериализует Python объект из файла формата yaml

        :param fp: str
        :return: object
        """
        obj = ""
        with open(fp, "r") as f:
            for line in f:
                obj += line
            dictionary = yaml.load(obj, Loader=yaml.Loader)

        return Serializer.object_deserialization(dictionary)

    @staticmethod
    def loads(s: str) -> Any:
        """
        Десериализует Python объект из строки формата yaml

        :param s: str
        :return: object
        """
        dictionary = yaml.load(s, Loader=yaml.Loader)
        return Serializer.object_deserialization(dictionary)
