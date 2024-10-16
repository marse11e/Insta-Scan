# -*- coding: utf-8 -*-
import lzma
import json
import os
import sys


def read_json_xz(file_path):
    try:
        with lzma.open(file_path, mode='rt', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except lzma.LZMAError:
        print("Ошибка: Некорректный формат файла. Убедитесь, что это .json.xz файл.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        sys.exit(1)


def save_json_to_file(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в {output_path}")


if __name__ == "__main__":
    file_path = 'data/raw/lavilin.com.kz/2024-02-24_08-38-57_UTC.json.xz'
    data = read_json_xz(file_path)
    output_directory = os.path.dirname(file_path)
    output_filename = os.path.basename(file_path).replace('.json.xz', '.json')
    output_path = os.path.join(output_directory, output_filename)
    save_json_to_file(data, output_path)


