#!/bin/bash

read -p "Введите имя пользователя БД: " db_user
read -p "Введите пароль пользователя БД: " db_password
echo
read -p "Введите имя схемы для импорта: " schema_name
read -p "Введите имя директории Data Pump: " dump_dir
read -p "Введите имя файла дампа (например, schema_exp.dmp): " dump_file

impdp "${db_user}/${db_password}" schemas="${schema_name}" directory="${dump_dir}" dumpfile="${dump_file}"  logfile="${schema_name}_import.log"

echo " Лог файл: ${schema_name}_import.log"

