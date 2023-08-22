#!/bin/bash

# Указываем путь к файлу
file_path='/etc/clickhouse-server/users.xml'

# Указываем строку для замены
old_string='<!-- <access_management>1</access_management> -->'
new_string='<access_management>1</access_management>'

# Заменяем строку в файле с помощью sed
sed -i "s|$old_string|$new_string|g" "$file_path"

sql_user="CREATE USER IF NOT EXISTS $CLICKHOUSE_USERNAME IDENTIFIED WITH PLAINTEXT_PASSWORD BY '$CLICKHOUSE_PASSWORD';"
sql_db="CREATE DATABASE IF NOT EXISTS $CLICKHOUSE_DB;"
sql_grant="GRANT ALL PRIVILEGES ON $CLICKHOUSE_DB.* TO $CLICKHOUSE_USERNAME;"

clickhouse-client -q "SYSTEM RELOAD CONFIG;"
clickhouse-client -q "$sql_user"
clickhouse-client -q "$sql_db"
clickhouse-client -q "$sql_grant"

sed -i "s|$new_string|$old_string|g" "$file_path"
