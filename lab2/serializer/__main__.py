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

    print('Convert was complited successfully')


parser = argparse.ArgumentParser(description='Сериализатор')
parser.add_argument('name', type=str, help='file name')
parser.add_argument('input_format', type=str, help='input format')
parser.add_argument('output_format', type=str, help='output format')

args = parser.parse_args()
convert_file(args.name, args.input_format, args.output_format)
