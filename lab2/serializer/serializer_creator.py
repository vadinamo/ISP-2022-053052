from serializer.serializer import Serializer
from serializer.json_serializer import JsonSerializer
from serializer.toml_serializer import TomlSerializer
from serializer.yaml_serializer import YamlSerializer

class SerializerCreator:
    """
    Класс создает тип сериализатора в зависимости от исходного формата
    """
    @staticmethod
    def create_serializer(format_name: str) -> Serializer:
        """
        Метод возвращает сериализатор в зависимости от исходного формата

        :param format_name:  str
        :return: Serializer
        """
        if format_name == 'json':
            return JsonSerializer

        elif format_name == 'toml':
            return TomlSerializer

        elif format_name == 'yaml':
            return YamlSerializer
