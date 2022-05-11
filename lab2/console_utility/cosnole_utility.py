import argparse
from serializer.serializer_creator import SerializerCreator
from pathlib import Path


def convert_file(file_name: str, from_format: str, to_format: str) -> None:
    """
    Функция конвертирует файл из исходного формата в указанный

    :param file_name: str
    :param from_format: str
    :param to_format: str
    :return: None
    """
    if from_format == to_format:
        return

    new_file_name = Path(file_name)
    new_file_name = new_file_name.stem + '.' + to_format

    input_serializer = SerializerCreator.create_serializer(from_format)
    output_serializer = SerializerCreator.create_serializer(to_format)

    deserialize = input_serializer.load(file_name)
    output_serializer.dump(deserialize, new_file_name)


def create_parser():
    """
    Создает parser консольной утилиты
    :return: Parser
    """
    parser = argparse.ArgumentParser(description='Сериализатор')
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('-i', type=str, required=True)
    parser.add_argument('-o', type=str, required=True)

    args = vars(parser.parse_args())
