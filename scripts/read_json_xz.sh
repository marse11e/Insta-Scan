#!/bin/bash

echo "Введите путь к файлу (.json.xz):"
read file_path

python_file="src/utils/read_json_xz.py"

sed -i "s|file_path = .*|file_path = '$file_path'|" $python_file

python3 $python_file

