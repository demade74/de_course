-- -----------------------------------------------------
-- Практическое задание по теме "Оптимизация запросов"
-- -----------------------------------------------------

-- Задание 1
/*
 * Создайте таблицу logs типа Archive. Пусть при каждом создании записи в таблицах users, catalogs и products 
 * в таблицу logs помещается время и дата создания записи, название таблицы, идентификатор первичного ключа и содержимое поля name 
 */

USE shop;
CREATE TABLE logs (
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	table_name VARCHAR(20) NOT NULL,
	pk_id INT NOT NULL,
	name VARCHAR(100) NULL
) ENGINE=ARCHIVE;

-- триггер на вставку в таблицу users
DROP TRIGGER IF EXISTS add_insert_log_users;
CREATE TRIGGER add_insert_log_users AFTER INSERT ON users
FOR EACH ROW
BEGIN
	INSERT logs
		(created_at, table_name, pk_id, name)
	VALUES 
		(NEW.created_at, 'users', NEW.id, NEW.name);
END

-- триггер на вставку в таблицу catalogs
DROP TRIGGER IF EXISTS add_insert_log_catalogs;
CREATE TRIGGER add_insert_log_catalogs AFTER INSERT ON catalogs
FOR EACH ROW
BEGIN
	INSERT logs
		(table_name, pk_id, name)
	VALUES 
		('catalogs', NEW.id, NEW.name);
END

-- триггер на вставку в таблицу products
DROP TRIGGER IF EXISTS add_insert_log_products;
CREATE TRIGGER add_insert_log_products AFTER INSERT ON products
FOR EACH ROW
BEGIN
	INSERT logs
		(created_at, table_name, pk_id, name)
	VALUES 
		(NEW.created_at, 'products', NEW.id, NEW.name);
END

INSERT users (name, birthday_at) VALUES ('Николай', '19900524');
INSERT catalogs (name) VALUES ('SSD накопители');
INSERT products (name, catalog_id) VALUES ('Motherboard', 2);

SELECT * FROM logs;
-- created_at         |table_name|pk_id|name          |
-- -------------------|----------|-----|--------------|
-- 2021-03-30 13:58:06|users     |    0|Константин    |
-- 2021-03-30 14:01:19|users     |    9|Николай       |
-- 2021-03-30 14:11:36|catalogs  |    6|SSD накопители|
-- 2021-03-30 14:11:38|products  |   16|Motherboard   |


-- Задание 2
-- Создайте SQL-запрос, который помещает в таблицу users миллион записей

-- Решение первое: через хранимую процедуру, в которой будем подготавливать строку с значениями для users для вставки, скажем, по 1000 за раз.
-- Данное решение отработает быстрее, чем построчная вставка значений. Это сократит время выполнения вставки.
-- Каждую 1000 раз накапливаем значения ('Пользователь', '1990-01-01') для вставки.
-- Каждый тысячный раз подготавливаем динамический запрос на вставку, выполняем его, очищаем данные и продолжаем итерации, пока не достигнем миллиона.
-- Так как задание не ставит условие на разнообразность имен и дат рождения, будем вставлять константные имя и дату рождения

DROP PROCEDURE IF EXISTS big_insert;
CREATE PROCEDURE big_insert()
BEGIN
	DECLARE query_string TEXT DEFAULT '';
	DECLARE counter INT DEFAULT 1;

	SET @start_time = CURTIME();
	
	WHILE counter <= 1000000 DO
		SET query_string = CONCAT(query_string, '(\'Пользователь\', \'1990-01-01\'), ');
		IF (counter % 1000) = 0 THEN
			SET @query = CONCAT('INSERT users (name, birthday_at) VALUES ', TRIM(TRAILING ', ' FROM query_string)); 
			PREPARE query FROM @query;
			EXECUTE query;
			DROP PREPARE query;
			SET @query = '';
			SET query_string = '';
		END IF;
		SET counter = counter + 1;
	END WHILE;
	SET @execution_time = TIMEDIFF(CURTIME(), @start_time);
END

CALL big_insert();
SELECT @execution_time;
-- @execution_time|
-- ---------------|
-- 00:01:02.000000|

SELECT COUNT(*) FROM users;
-- COUNT(*)|
-- --------|
--  1000006|

-- Решение второе: вставка данных из файла.
-- С помощью написанного мной скрипта на python сгенерировал csv файл на миллион записей.
-- Командой LOAD DATA LOCAL INFILE произведена операция вставки записей, время выполнения составило 25 секунд, что в 2 раза быстрее вставки процедурой
-- P.S. Для того, чтобы загрузку можно было произвести, включены две настройки, а именно:
-- local_infile = ON на стороне сервера и allowLoadLocalInfile = true на стороне клиента


-- delete from users where name = 'Пользователь';
-- delete from users where id > 1000000;

SET GLOBAL local_infile = ON;
LOAD DATA LOCAL INFILE 'C:\\Program Files\\MySQL\\MySQL Server 8.0\\etc\\users.csv' 
INTO TABLE users
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
(name, birthday_at);
-- 25 sec
