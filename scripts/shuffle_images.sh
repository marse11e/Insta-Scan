#!/bin/bash

read -p "Введите имя пользователя: " from_path_username

raw_folder="data/raw/${from_path_username}"
processed_folder="data/processed/${from_path_username}_img"

mkdir -p "${processed_folder}"

find "${raw_folder}" -type f \( -iname "*.jpg" -o -iname "*.png" \) | shuf | while read -r file; do
    mv "$file" "${processed_folder}/"
done

echo "Файлы перемешаны и перемещены в ${processed_folder}"
