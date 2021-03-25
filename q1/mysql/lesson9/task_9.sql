------------------------------------------------------------------------
-- Практическое задание по теме "Транзакции, переменные, представления"
------------------------------------------------------------------------
-- Задание 1
-- В базе данных shop и sample присутствуют одни и те же таблицы, учебной базы данных. 
-- Переместите запись id = 1 из таблицы shop.users в таблицу sample.users. Используйте транзакции.

-- Таблица sample.users содержит 2 столбца: id, name
-- Добавим атрибуты birthday, created_at, updated_at чтобы сохранить всю имеющуюся информацию

ALTER TABLE sample.users
ADD (
	birthday DATE NOT NULL,
	created_at DATETIME DEFAULT CURTIME()STAMP,
	updated_at DATETIME DEFAULT CURTIME()STAMP ON UPDATE CURTIME()STAMP
);

START TRANSACTION;
INSERT INTO sample.users (id, name, birthday, created_at, updated_at)
	SELECT u.id, u.name, u.birthday_at, u.created_at, u.updated_at
	FROM shop.users AS u WHERE u.id = 1;
	
DELETE FROM shop.users
WHERE id = 1;
COMMIT;

-- Задание 2
-- Создайте представление, которое выводит название name товарной позиции из таблицы products и соответствующее название каталога name из таблицы catalogs.

CREATE VIEW shop.cat AS
	SELECT p.name AS product_name, p.description, c.name AS catalog_name
	  FROM shop.products p
	  JOIN shop.catalogs c
	    ON p.catalog_id = c.id;
	  
SELECT * FROM shop.cat;
-- product_name           |description                                                                      |catalog_name     |
-- -----------------------|---------------------------------------------------------------------------------|-----------------|
-- Intel Core i3-8100     |Процессор для настольных персональных компьютеров, основанных на платформе Intel.|Процессоры       |
-- Intel Core i5-7400     |Процессор для настольных персональных компьютеров, основанных на платформе Intel.|Процессоры       |
-- AMD FX-8320E           |Процессор для настольных персональных компьютеров, основанных на платформе AMD.  |Процессоры       |
-- AMD FX-8320            |Процессор для настольных персональных компьютеров, основанных на платформе AMD.  |Процессоры       |
-- ASUS ROG MAXIMUS X HERO|Материнская плата ASUS ROG MAXIMUS X HERO, Z370, Socket 1151-V2, DDR4, ATX       |Материнские платы|
-- Gigabyte H310M S2H     |Материнская плата Gigabyte H310M S2H, H310, Socket 1151-V2, DDR4, mATX           |Материнские платы|
-- MSI B250M GAMING PRO   |Материнская плата MSI B250M GAMING PRO, B250, Socket 1151, DDR4, mATX            |Материнские платы|


-- Задание 3
-- Пусть имеется таблица с календарным полем created_at. В ней размещены разряженые календарные записи за август 2018 года:
-- '2018-08-01', '2018-08-04', '2018-08-16' и 2018-08-17. Составьте запрос, который выводит полный список дат за август, 
-- выставляя в соседнем поле значение 1, если дата присутствует в исходной таблице и 0, если она отсутствует.

CREATE TABLE shop.date_table (created_at DATE);
INSERT shop.date_table VALUES ('2018-08-01'), ('2018-08-04'), ('2018-08-16'), ('2018-08-17');

WITH RECURSIVE august_days (`date`, ex) AS (
	SELECT @cur_date := '2018-08-01', @value_exists := @cur_date IN (SELECT * FROM shop.date_table)
	UNION ALL
	SELECT @cur_date := @cur_date + INTERVAL 1 DAY, @value_exists := @cur_date IN (SELECT * FROM shop.date_table)
	FROM august_days
	WHERE `date` < '2018-08-31'
)

SELECT * FROM august_days
-- date      |ex|
-- ----------|--|
-- 2018-08-01| 1|
-- 2018-08-02| 0|
-- 2018-08-03| 0|
-- 2018-08-04| 1|
-- 2018-08-05| 0|
-- 2018-08-06| 0|
-- 2018-08-07| 0|
-- 2018-08-08| 0|
-- 2018-08-09| 0|
-- 2018-08-10| 0|
-- 2018-08-11| 0|
-- 2018-08-12| 0|
-- 2018-08-13| 0|
-- 2018-08-14| 0|
-- 2018-08-15| 0|
-- 2018-08-16| 1|
-- 2018-08-17| 1|
-- 2018-08-18| 0|
-- 2018-08-19| 0|
-- 2018-08-20| 0|
-- 2018-08-21| 0|
-- 2018-08-22| 0|
-- 2018-08-23| 0|
-- 2018-08-24| 0|
-- 2018-08-25| 0|
-- 2018-08-26| 0|
-- 2018-08-27| 0|
-- 2018-08-28| 0|
-- 2018-08-29| 0|
-- 2018-08-30| 0|
-- 2018-08-31| 0|

-- Задание 4
-- Пусть имеется любая таблица с календарным полем created_at. 
-- Создайте запрос, который удаляет устаревшие записи из таблицы, оставляя только 5 самых свежих записей.

INSERT shop.date_table VALUES ('2019-07-03'), ('2015-08-04'), ('2012-08-16'), ('2020-08-17'), ('2017-08-17'), ('2021-02-17');
SELECT created_at 
  FROM shop.date_table
 ORDER BY created_at DESC;

-- Способ 1: Удалим все записи из таблицы где дата не в списке 5 самых свежих
DELETE FROM shop.date_table
 WHERE created_at NOT IN 
 	(SELECT * 
 	   FROM (SELECT created_at
 	           FROM shop.date_table
 	          ORDER BY created_at DESC
 	          LIMIT 5
 	        ) t
 	);

-- Способ 2: Сохраним в переменную @dates последнюю самую свежую дату из 5 и удалим все записи, которые идут раньше нее
SELECT @dates := created_at FROM shop.date_table ORDER BY created_at DESC LIMIT 5;
DELETE FROM shop.date_table
 WHERE created_at < @dates

----------------------------------------------------------
-- Практическое задание по теме "Администрирование MySQL"
----------------------------------------------------------
-- Задание 1
/* Создайте двух пользователей которые имеют доступ к базе данных shop.
 * Первому пользователю shop_read должны быть доступны только запросы на чтение данных, 
 * второму пользователю shop — любые операции в пределах базы данных shop
 */
USE shop;
CREATE USER 'shop_read'@'localhost';
CREATE USER 'shop_all'@'localhost';
SELECT `host`, `user` FROM mysql.`user`;

-- host     |user            |
-- ---------|----------------|
-- localhost|mysql.infoschema|
-- localhost|mysql.session   |
-- localhost|mysql.sys       |
-- localhost|root            |
-- localhost|shop_all        |
-- localhost|shop_read       |

-- Первому пользователю даны права только на чтение в пределах БД shop
GRANT SELECT ON shop.* TO 'shop_read'@'localhost';
-- При попытке обновить запись, получаем сообщение об ошибке - работает
-- mysql> update users set name = 'Марина' where id = 2;
-- ERROR 1142 (42000): UPDATE command denied to user 'shop_read'@'localhost' for table 'users'

-- Второму пользователю даны права на любые действия, но в пределах БД shop
GRANT ALL ON shop.* TO 'shop_all'@'localhost';

-- Пользователь может обновить запись
-- mysql> use shop;
-- Database changed
-- mysql> update users set name = 'Марина' where id = 2;
-- Query OK, 1 row affected (0.01 sec)
-- Rows matched: 1  Changed: 1  Warnings: 0
-- 
-- mysql> select * from users;
-- +----+-----------+-------------+---------------------+---------------------+
-- | id | name      | birthday_at | created_at          | updated_at          |
-- +----+-----------+-------------+---------------------+---------------------+
-- |  2 | Марина    | 1984-11-12  | 2021-03-24 21:22:36 | 2021-03-24 21:22:36 |
-- |  3 | Александр | 1985-05-20  | 2017-10-24 08:10:00 | 2017-10-25 08:10:00 |
-- |  4 | Сергей    | 1988-02-14  | 2017-11-20 08:10:00 | 2017-11-21 08:10:00 |
-- |  5 | Иван      | 1998-01-12  | 2017-11-25 08:10:00 | 2017-10-26 08:10:00 |
-- |  6 | Мария     | 1992-02-29  | 2021-03-10 23:36:28 | 2021-03-10 23:36:28 |
-- +----+-----------+-------------+---------------------+---------------------+
-- 5 rows in set (0.00 sec)

-- Но при попытке переключиться на другую БД доступ запрещен
-- mysql> use sample;
-- ERROR 1044 (42000): Access denied for user 'shop_all'@'localhost' to database 'sample'

-- Задание 2
/* Пусть имеется таблица accounts содержащая три столбца id, name, password, содержащие первичный ключ, имя пользователя и его пароль.
 * Создайте представление username таблицы accounts, предоставляющий доступ к столбца id и name. 
 * Создайте пользователя user_read, который бы не имел доступа к таблице accounts, однако, мог бы извлекать записи из представления username
 */
USE shop;
CREATE TABLE accounts (
	acc_id SERIAL PRIMARY KEY,
	name VARCHAR(20) DEFAULT NULL,
	pwd VARCHAR(256) DEFAULT (SHA2('abc', 256))
);
INSERT accounts (acc_id, name) VALUES (NULL, 'acc1'), (NULL, 'acc2'), (NULL, 'acc3'), (NULL, 'acc4'), (NULL, 'acc5');

CREATE VIEW username AS
	SELECT acc_id, name
	  FROM accounts;

-- Согласно задания просто создаем пользователя (по умолчанию у новых пользователей нет никаких прав, что достаточно для того, чтобы
-- новый пользователь не смог обратиться к таблице accounts) и даем доступ на чтение для представления username	 
CREATE USER user_read;
GRANT SELECT ON shop.username TO user_read;

-- mysql> use shop;
-- Database changed
-- mysql> select * from username;
-- +--------+------+
-- | acc_id | name |
-- +--------+------+
-- |      1 | acc1 |
-- |      2 | acc2 |
-- |      3 | acc3 |
-- |      4 | acc4 |
-- |      5 | acc5 |
-- +--------+------+
-- 5 rows in set (0.01 sec)
-- 
-- mysql> select * from accounts;
-- ERROR 1142 (42000): SELECT command denied to user 'user_read'@'localhost' for table 'accounts'

-------------------------------------------------------------------------
-- Практическое задание по теме "Хранимые процедуры и функции, триггеры"
-------------------------------------------------------------------------
/*
 * Создайте хранимую функцию hello(), которая будет возвращать приветствие, в зависимости от текущего времени суток. 
 * С 6:00 до 12:00 функция должна возвращать фразу "Доброе утро", с 12:00 до 18:00 функция должна возвращать фразу "Добрый день", 
 * с 18:00 до 00:00 — "Добрый вечер", с 00:00 до 6:00 — "Доброй ночи".
 */

-- DELIMITER $$
DROP PROCEDURE IF EXISTS hello;
CREATE PROCEDURE hello()
BEGIN
	DECLARE user_name VARCHAR(50) DEFAULT (SUBSTRING_INDEX(USER(), '@', 1));
	
	IF(CURTIME() >= '06:00:00' AND CURTIME() < '12:00:00') THEN
		SELECT CONCAT('Доброе утро, ', user_name) AS 'greeting';
	ELSEIF(CURTIME() >= '12:00:00' AND CURTIME() < '18:00:00') THEN
		SELECT CONCAT('Доброе день, ', user_name) AS 'greeting';
	ELSEIF(CURTIME() >= '18:00:00' AND CURTIME() <= '23:59:59') THEN
		SELECT CONCAT('Доброе вечер, ', user_name) AS 'greeting';
	ELSE
		SELECT CONCAT('Доброй ночи, ', user_name) AS 'greeting';
	END IF;
END
-- DELIMITER ;

CALL hello();
-- greeting         |
-- -----------------|
-- Доброе день, root|

-- Задание 2
/*
 * В таблице products есть два текстовых поля: name с названием товара и description с его описанием. 
 * Допустимо присутствие обоих полей или одно из них. Ситуация, когда оба поля принимают неопределенное значение NULL неприемлема. 
 * Используя триггеры, добейтесь того, чтобы одно из этих полей или оба поля были заполнены. 
 * При попытке присвоить полям NULL-значение необходимо отменить операцию 
 */

USE shop;
DROP TRIGGER IF EXISTS check_input_products;
CREATE TRIGGER check_input_products BEFORE INSERT ON products
FOR EACH ROW
BEGIN
	DECLARE null_name TINYINT;
	DECLARE null_description TINYINT;
	
	SET null_name = ISNULL(NEW.name);
	SET null_description = ISNULL(NEW.description);
	
	IF (null_name + null_description) = 2 THEN
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'DELETE canceled';
	END IF;
END

-- case 1: name == null - OK
INSERT INTO products
	(id, name, description, price)
VALUES
	(NULL, NULL, 'description1', 1200.0)
	
-- case 2: description == null - OK
INSERT INTO products
	(id, name, description, price)
VALUES
	(NULL, 'name2', NULL, 1300.0)
	
-- case 3: name and description == null - OK
INSERT INTO products
	(id, name, description, price)
VALUES
	(NULL, NULL, NULL, 1400.0)
-- SQL Error [1644] [45000]: DELETE canceled
	
-- Задание 3
/*
 * Напишите хранимую функцию для вычисления произвольного числа Фибоначчи. 
 * Числами Фибоначчи называется последовательность в которой число равно сумме двух предыдущих чисел. 
 * Вызов функции FIBONACCI(10) должен возвращать число 55 
 */
	
DROP FUNCTION IF EXISTS FIBONACCI;
CREATE FUNCTION FIBONACCI(num INT)
RETURNS BIGINT DETERMINISTIC
BEGIN
	SET @a = 0;
	SET @b = 1;
	SET @counter = 1;

	IF num < 0 THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'argument must be positive number';END IF;
	IF num = 0 THEN RETURN @a;END IF;
	IF num = 1 THEN RETURN @b;END IF;

	WHILE @counter < num DO
		SET @c = @a + @b;
		SET @a = @b;
		SET @b = @c;
		SET @counter = @counter + 1;
	END WHILE;
	RETURN @c;
END

SELECT FIBONACCI(10);
-- FIBONACCI(10)|
-- -------------|
--            55|