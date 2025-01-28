
# Часть 2. СУБД Oracle.

### 2. Создайте пользователей с различными уровнями привилегий (администратор базы данных, пользователь, ограниченный пользователь (только чтение данных)). Каждому пользователю назначьте отдельное табличное пространство.
##### Commnads
`create tablespace admin_tblspace datafile 'admin_tblspace.dbf' size 100M;` -- Создание табличного пространства для пользователя admin 
`create tablespace user_tblspace datafile 'user_tblspace.dbf' size 100M; ` -- Создание табличного пространства для пользователя simpl_user 
`create tablespace reader_tblspace datafile 'reader_tblspace' size 100M;` -- Создание табличного пространства для пользователя reader_user 
`create user admin identified by 2024 default tablespace admin_tblspace;` -- Создание пользователя admin с указанием пароля и табличного пространства 
`grant dba to admin;` -- Предоставление прав администратора пользователю 
`admin create user simpl_user identified by 2024 default tablespace user_tblspace;`-- Создание пользователя simpl_user с паролем и табличным пространством
`grant create session to simpl_user`; -- Разрешение пользователю simpl_user создавать сессии 
`grant create table to simpl_user;` -- Разрешение пользователю simpl_user создавать таблицы
`grant create view to simpl_user;` -- Разрешение пользователю simpl_user создавать представления 
`create user reader_user identified by 2024 default tablespace reader_tblspace;` -- Создание пользователя reader_user с паролем и табличным пространством
`grant create session to reader_user;` -- Разрешение пользователю reader_user создавать сессии 
`grant select any table to reader_user; `-- Разрешение пользователю reader_user читать любые таблицы

History
``` sql
-- Создание табличного пространства для трех ползователей 
SQL> create tablespace admin_tblspace datafile 'admin_tblspace.dbf' size 100M; 

Tablespace created.

SQL> create tablespace user_tblspace datafile 'user_tblspace.dbf' size 100M;

Tablespace created.

SQL> create tablespace reader_tblspace datafile 'reader_tblspace' size 100M;

Tablespace created.

SQL> create user admin identified by 2024 default tablespace admin_tblspace;

User created.

SQL> grant dba to admin; -- Права администатора пользователю админ

Grant succeeded.

SQL> create user simpl_user identified by 2024 default tablespace user_tblspace;

User created.

SQL> grant create session to simpl_user; --создании сессии пользователю 

Grant succeeded.

SQL> grant create table to simpl_user;

Grant succeeded.

SQL> grant create view to simpl_user;

Grant succeeded.

SQL> create user reader_user identified by 2024 default tablespace reader_tblspace;

User created.

SQL> grant create session to reader_user;

Grant succeeded.

SQL> grant select any table to reader_user;

Grant succeeded.

```


### 3. Для каждого пользователя создайте таблицы и наполните их данными. 

1. Создание и заполнение для админа

```sql
-- Создание таблицы для администраторов
CREATE TABLE admin_users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    created_at DATE DEFAULT SYSDATE
);

-- Вставка данных в таблицу
INSERT INTO admin_users (user_id, username, email)
VALUES (1, 'admin_john', 'admin_john@example.com');

INSERT INTO admin_users (user_id, username, email)
VALUES (2, 'admin_alex', 'admin_alex@example.com');

-- Создание другой таблицы для управления пользователями
CREATE TABLE user_roles (
    role_id NUMBER PRIMARY KEY,
    role_name VARCHAR2(100) NOT NULL
);

-- Вставка данных в таблицу
INSERT INTO user_roles (role_id, role_name)
VALUES (1, 'admin');

INSERT INTO user_roles (role_id, role_name)
VALUES (2, 'reader');

INSERT INTO user_roles (role_id, role_name)
VALUES (3, 'simpl_user');

```

---

2. Для reader
 
```sql
-- Создание таблицы для читателей
CREATE TABLE reader_users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    joined_at DATE DEFAULT SYSDATE
);

-- Вставка данных
INSERT INTO reader_users (user_id, username, email)
VALUES (1, 'reader_mary', 'reader_mary@example.com');

INSERT INTO reader_users (user_id, username, email)
VALUES (2, 'reader_luke', 'reader_luke@example.com');

```


---

3. Для simpl_user

```sql
-- Создание таблицы для упрощённых пользователей
CREATE TABLE simpl_users (
    user_id NUMBER PRIMARY KEY,
    username VARCHAR2(100) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    registration_date DATE DEFAULT SYSDATE
);

-- Вставка данных
INSERT INTO simpl_users (user_id, username, email)
VALUES (1, 'simpl_user_anna', 'simpl_user_anna@example.com');

INSERT INTO simpl_users (user_id, username, email)
VALUES (2, 'simpl_user_ivan', 'simpl_user_ivan@example.com');

```

### 4. Создайте скрипт для экспорта одной любой схемы с помощью инструмента data pump. Опишите также процесс импорта этой схемы.
#### Process
###### Экспорт схемы:

1. **Запуск скрипта `export_schema.sh`**: Пользователь вводит данные для подключения к базе данных (имя пользователя, пароль) и указывает схему для экспорта (например, `simpl_user`).
2. **Создание дампа**: Утилита Data Pump (через команду `expdp`) начинает экспорт данных из схемы `simpl_user` в файл дампа (`schema_exp1.dmp`), используя указанное табличное пространство для записи дампа.
3. **Завершение экспорта**: Экспорт завершён успешно за 14 секунд, создавая дамп-файл `/home/oracle/datapump_backup/schema_exp1.dmp`.

###### Импорт схемы:

1. **Запуск скрипта `import_schema.sh`**: Импортировать схему с помощью утилиты Data Pump (через команду `impdp`).
2. Намеренные ошибки:
    
    - **Ошибка 1**: В файле дампа указана схема с ошибкой в имени (`siml_user` вместо `simpl_user`), что приводит к ошибке `ORA-39165: Schema SIML_USER was not found`.
    - **Ошибка 2**: При попытке импорта схемы `simpl_user` возникает ошибка `ORA-01950: no privileges on tablespace 'USER_TBLSPACE'`, указывающая на отсутствие прав у пользователя на указанное табличное пространство.
    - **Ошибка 3**: При попытке импорта в схему, которая уже существует, возникает ошибка `ORA-31684: Object type USER:"SIMPL_USER" already exists`.
4. **Удаление пользователя**: Для решения проблем с существующей схемой (`simpl_user`), пользователь удаляет её через SQL*Plus с командой `DROP USER simpl_user CASCADE`, удаляя пользователя и его объекты.
    
5. **Повторный запуск импорта**: После удаления схемы и очистки, скрипт импорта запускается снова. Этот раз импорт проходит успешно, и все объекты из дампа корректно восстанавливаются в схему `simpl_user`.

> скрипты приложены  export_schema.sh и import_schema.sh


History
```bash
[oracle@Linux datapump_scripts]$ ./export_schema.sh
Введите имя пользователя БД: admin
Введите пароль пользователя БД: 2024

Введите имя схемы для экспорта: simpl_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema_exp1.dmp

Export: Release 19.0.0.0.0 - Production on Tue Jan 28 07:35:23 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Starting "ADMIN"."SYS_EXPORT_SCHEMA_01":  admin/******** schemas=simpl_user directory=datapump_dir dumpfile=schema_exp1.dmp
Processing object type SCHEMA_EXPORT/USER
Processing object type SCHEMA_EXPORT/SYSTEM_GRANT
Processing object type SCHEMA_EXPORT/DEFAULT_ROLE
Processing object type SCHEMA_EXPORT/PRE_SCHEMA/PROCACT_SCHEMA
Master table "ADMIN"."SYS_EXPORT_SCHEMA_01" successfully loaded/unloaded
******************************************************************************
Dump file set for ADMIN.SYS_EXPORT_SCHEMA_01 is:
  /home/oracle/datapump_backup/schema_exp1.dmp
Job "ADMIN"."SYS_EXPORT_SCHEMA_01" successfully completed at Tue Jan 28 07:35:41 2025 elapsed 0 00:00:14

[oracle@Linux datapump_scripts]$ nano export_schema.sh
[oracle@Linux datapump_scripts]$ nano import_schema.sh
[oracle@Linux datapump_scripts]$
[oracle@Linux datapump_scripts]$ ./import_schema.sh
Введите имя пользователя БД: admin
Введите пароль пользователя БД: 2024

Введите имя схемы для импорта: siml_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema_exp1.dmp

Import: Release 19.0.0.0.0 - Production on Tue Jan 28 07:39:03 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
ORA-39002: invalid operation
ORA-39165: Schema SIML_USER was not found.

 Лог файл: siml_user_import.log
[oracle@Linux datapump_scripts]$ ./import_schema.sh
Введите имя пользователя БД: simpl_user
Введите пароль пользователя БД: 2024

Введите имя схемы для импорта: simpl_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema_exp1.dmp

Import: Release 19.0.0.0.0 - Production on Tue Jan 28 07:41:01 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
ORA-31626: job does not exist
ORA-31633: unable to create master table "SIMPL_USER.SYS_IMPORT_SCHEMA_05"
ORA-06512: at "SYS.DBMS_SYS_ERROR", line 95
ORA-06512: at "SYS.KUPV$FT", line 1163
ORA-01950: no privileges on tablespace 'USER_TBLSPACE'
ORA-06512: at "SYS.KUPV$FT", line 1056
ORA-06512: at "SYS.KUPV$FT", line 1044


 Лог файл: simpl_user_import.log
[oracle@Linux datapump_scripts]$ ./import_schema.sh
Введите имя пользователя БД: admin
Введите пароль пользователя БД: 2024

Введите имя схемы для импорта: simpl_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema1_exp.dmp

Import: Release 19.0.0.0.0 - Production on Tue Jan 28 07:42:02 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
ORA-39001: invalid argument value
ORA-39000: bad dump file specification
ORA-31640: unable to open dump file "/home/oracle/datapump_backup/schema1_exp.dmp" for read
ORA-27037: unable to obtain file status
Linux-x86_64 Error: 2: No such file or directory
Additional information: 7


 Лог файл: simpl_user_import.log
[oracle@Linux datapump_scripts]$ cd
[oracle@Linux ~]$ cd datapump_backup/
[oracle@Linux datapump_backup]$ ls
export.log  schema_exp1.dmp  siml_user_import.log  simpl_user_import.log
[oracle@Linux datapump_backup]$ cd
[oracle@Linux ~]$ cd datapump_scripts/
[oracle@Linux datapump_scripts]$ ./import_schema.sh
Введите имя пользователя БД: admin
Введите пароль пользователя БД: 2024

Введите имя схемы для импорта: simpl_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema_exp1.dmp

Import: Release 19.0.0.0.0 - Production on Tue Jan 28 07:43:37 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Master table "ADMIN"."SYS_IMPORT_SCHEMA_01" successfully loaded/unloaded
Starting "ADMIN"."SYS_IMPORT_SCHEMA_01":  admin/******** schemas=simpl_user directory=datapump_dir dumpfile=schema_exp1.dmp logfile=simpl_user_import.log
Processing object type SCHEMA_EXPORT/USER
ORA-31684: Object type USER:"SIMPL_USER" already exists

Processing object type SCHEMA_EXPORT/SYSTEM_GRANT
Processing object type SCHEMA_EXPORT/DEFAULT_ROLE
Processing object type SCHEMA_EXPORT/PRE_SCHEMA/PROCACT_SCHEMA
Job "ADMIN"."SYS_IMPORT_SCHEMA_01" completed with 1 error(s) at Tue Jan 28 07:43:40 2025 elapsed 0 00:00:02

 Лог файл: simpl_user_import.log
[oracle@Linux datapump_scripts]$ cd
[oracle@Linux ~]$
[oracle@Linux ~]$
[oracle@Linux ~]$ sqlplus / as sysdba

SQL*Plus: Release 19.0.0.0.0 - Production on Tue Jan 28 07:50:30 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.


Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

SQL>
SQL> drop user simpl_user cascade;

User dropped.

SQL> SELECT username FROM dba_users WHERE username = 'simpl_user';


no rows selected

SQL> SQL> exit
Disconnected from Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0
[oracle@Linux ~]$ cd datapump_scripts/
[oracle@Linux datapump_scripts]$ ./import_schema.sh
Введите имя пользователя БД: admin
Введите пароль пользователя БД: 2024

Введите имя схемы для импорта: simpl_user
Введите имя директории Data Pump: datapump_dir
Введите имя файла дампа (например, schema_exp.dmp): schema_exp1.dmp

Import: Release 19.0.0.0.0 - Production on Tue Jan 28 07:52:40 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle and/or its affiliates.  All rights reserved.

Connected to: Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Master table "ADMIN"."SYS_IMPORT_SCHEMA_01" successfully loaded/unloaded
Starting "ADMIN"."SYS_IMPORT_SCHEMA_01":  admin/******** schemas=simpl_user directory=datapump_dir dumpfile=schema_exp1.dmp logfile=simpl_user_import.log
Processing object type SCHEMA_EXPORT/USER
Processing object type SCHEMA_EXPORT/SYSTEM_GRANT
Processing object type SCHEMA_EXPORT/DEFAULT_ROLE
Processing object type SCHEMA_EXPORT/PRE_SCHEMA/PROCACT_SCHEMA
Job "ADMIN"."SYS_IMPORT_SCHEMA_01" successfully completed at Tue Jan 28 07:52:43 2025 elapsed 0 00:00:02

 Лог файл: simpl_user_import.log
[oracle@Linux datapump_scripts]$

```


### 5. Попробуйте создать rman скрипт для бэкапа всей базы данных. Осуществите запуск rman-скрипта из cron-а. Опишите скрипт, процесс запуска, покажите логи выполнения скрипта. 

#### Process
### Объяснение команд RMAN:

1. **`rman target /`**: Запуск RMAN и подключение к базе данных с использованием текущего пользователя
    
2. **`log='/home/oracle/rman_backup/rman_backup.log'`**: Указание пути для логирования выполнения резервного копирования. Лог будет храниться в `/home/oracle/rman_backup/rman_backup.log`.
    
3. **`allocate channel ch1 device type disk;`**: Выделение канала (channel) для резервного копирования на диск. Это указывает, что резервное копирование будет происходить на дисковое устройство.
    
4. **`backup database plus archivelog format '/home/oracle/rman_backup/%d_%s_%U.bkp';`**: Выполнение резервного копирования базы данных вместе с архивными журналами (archivelog) с указанным форматом имени файлов. 
	 - `%d` - имя  бд
	 - `%s`  - номер сбора
	 - `%U` -уникальный идентификатор
    
5. **`release channel ch1;`**: Освобождение канала, который использовался для резервного копирования.
    
6. **`exit`**: Завершение работы с RMAN.
    

Этот скрипт используется для выполнения резервного копирования базы данных с архивными журналами в папку `/home/oracle/rman_backup/`.

### Пример использования cron для автоматизации:

Для того чтобы автоматически запускать резервное копирование с помощью RMAN, можно использовать планировщик задач `cron`:

1. **Редактирование crontab**: Откройте crontab для редактирования:
``` bash
    crontab -e    
	```
       
2. **Добавление задачи**: Добавьте строку для запуска вашего скрипта, например, каждый день в 2:00:
``` bash
   1 * * * /home/oracle/rman_backup.sh
```    
 
### Объяснение cron:

- **`1 * * *`**: Это синтаксис cron, который указывает на выполнение задачи в  00:01, 01:01, ..., 23:01 каждый день
- **`/home/oracle/rman_backup/rman_backup.sh`**: Путь к  скрипту, который будет выполняться.

Используя cron, можно автоматизировать процесс резервного копирования и избавить себя от необходимости запускать его вручную.

```bash
[oracle@Linux ~]$ nano rman_backup.sh
[oracle@Linux ~]$ ./rman_backup.sh
RMAN> 2> 3> 4> 5> 6> 7> 8> RMAN> [oracle@Linux ~]$ cd rman_backup/
[oracle@Linux rman_backup]$ nano rman_backup.log
[oracle@Linux rman_backup]$ cd
[oracle@Linux ~]$ nano rman_backup.log
[oracle@Linux ~]$ nano rman_backup.sh
[oracle@Linux ~]$ nano rman_backup.log
[oracle@Linux ~]$ nano rman_backup.sh
[oracle@Linux ~]$ sqlplus / as sysdba

SQL*Plus: Release 19.0.0.0.0 - Production on Tue Jan 28 08:41:56 2025
Version 19.3.0.0.0

Copyright (c) 1982, 2019, Oracle.  All rights reserved.


Connected to:
Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0

SQL> select log_mode from v$database;

LOG_MODE
------------
NOARCHIVELOG

SQL> ^Cshutdown immediate;

SQL> shutdown immediate;
Database closed.
Database dismounted.
ORACLE instance shut down.
SQL> startup mount;
ORACLE instance started.

Total System Global Area 1593831936 bytes
Fixed Size                  8897024 bytes
Variable Size             436207616 bytes
Database Buffers         1140850688 bytes
Redo Buffers                7876608 bytes
Database mounted.
SQL> alter database archivelog;

Database altered.

SQL> alter database archivelog;

Database altered.

SQL> alter database open;

Database altered.

SQL> select log_mode from v$database;

LOG_MODE
------------
ARCHIVELOG

SQL> exit
Disconnected from Oracle Database 19c Enterprise Edition Release 19.0.0.0.0 - Production
Version 19.3.0.0.0
[oracle@Linux ~]$ ./rman_backup.sh
RMAN> 2> 3> 4> 5> 6> 7> 8> RMAN> [oracle@Linux ~]$ cd rman_backup/
[oracle@Linux rman_backup]$ nano
rman_backup.log            TESTDB_1_013gbub3_1_1.bkp  TESTDB_3_033gbubb_1_1.bkp

```
