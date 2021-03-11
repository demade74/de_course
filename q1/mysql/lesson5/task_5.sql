-- Создание БД
CREATE DATABASE IF NOT EXISTS shop;
USE shop;

-- Создание и заполнение таблицы catalogs
DROP TABLE IF EXISTS catalogs;
CREATE TABLE catalogs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Название раздела',
  UNIQUE unique_name(name(10))
) COMMENT = 'Разделы интернет-магазина';

INSERT INTO catalogs VALUES
  (NULL, 'Процессоры'),
  (NULL, 'Материнские платы'),
  (NULL, 'Видеокарты'),
  (NULL, 'Жесткие диски'),
  (NULL, 'Оперативная память');

-- Создание и заполнение таблицы users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Имя покупателя',
  birthday_at DATE COMMENT 'Дата рождения',
  created_at VARCHAR(50) NULL,
  updated_at VARCHAR(50) NULL
) COMMENT = 'Покупатели';

INSERT INTO users (name, birthday_at, created_at, updated_at) VALUES
  ('Геннадий', '1990-10-05', '20.10.2017 8:10', '21.10.2017 8:10'),
  ('Наталья', '1984-11-12', '22.10.2017 8:10', '23.10.2017 8:10'),
  ('Александр', '1985-05-20', '24.10.2017 8:10', '25.10.2017 8:10'),
  ('Сергей', '1988-02-14', '20.11.2017 8:10', '21.11.2017 8:10'),
  ('Иван', '1998-01-12', '25.11.2017 8:10', '26.10.2017 8:10'),
  ('Мария', '1992-08-29', '22.12.2017 8:10', '24.12.2017 8:10');

-- Создание и заполнение таблицы products
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Название',
  description TEXT COMMENT 'Описание',
  price DECIMAL (11,2) COMMENT 'Цена',
  catalog_id INT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_catalog_id (catalog_id)
) COMMENT = 'Товарные позиции';

INSERT INTO products
  (name, description, price, catalog_id)
VALUES
  ('Intel Core i3-8100', 'Процессор для настольных персональных компьютеров, основанных на платформе Intel.', 7890.00, 1),
  ('Intel Core i5-7400', 'Процессор для настольных персональных компьютеров, основанных на платформе Intel.', 12700.00, 1),
  ('AMD FX-8320E', 'Процессор для настольных персональных компьютеров, основанных на платформе AMD.', 4780.00, 1),
  ('AMD FX-8320', 'Процессор для настольных персональных компьютеров, основанных на платформе AMD.', 7120.00, 1),
  ('ASUS ROG MAXIMUS X HERO', 'Материнская плата ASUS ROG MAXIMUS X HERO, Z370, Socket 1151-V2, DDR4, ATX', 19310.00, 2),
  ('Gigabyte H310M S2H', 'Материнская плата Gigabyte H310M S2H, H310, Socket 1151-V2, DDR4, mATX', 4790.00, 2),
  ('MSI B250M GAMING PRO', 'Материнская плата MSI B250M GAMING PRO, B250, Socket 1151, DDR4, mATX', 5060.00, 2);

-- Создание и заполнение таблицы orders
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_user_id(user_id)
) COMMENT = 'Заказы';

-- Создание и заполнение таблицы orders_products
DROP TABLE IF EXISTS orders_products;
CREATE TABLE orders_products (
  id SERIAL PRIMARY KEY,
  order_id INT UNSIGNED,
  product_id INT UNSIGNED,
  total INT UNSIGNED DEFAULT 1 COMMENT 'Количество заказанных товарных позиций',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = 'Состав заказа';

-- Создание и заполнение таблицы discounts
DROP TABLE IF EXISTS discounts;
CREATE TABLE discounts (
  id SERIAL PRIMARY KEY,
  user_id INT UNSIGNED,
  product_id INT UNSIGNED,
  discount FLOAT UNSIGNED COMMENT 'Величина скидки от 0.0 до 1.0',
  started_at DATETIME,
  finished_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_user_id(user_id),
  KEY index_of_product_id(product_id)
) COMMENT = 'Скидки';

-- Создание и заполнение таблицы storehouses
DROP TABLE IF EXISTS storehouses;
CREATE TABLE storehouses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT 'Название',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = 'Склады';

INSERT INTO storehouses 
	(id, name)
VALUES 
	(NULL, 'storehouse 1'),
	(NULL, 'storehouse 2'),
	(NULL, 'storehouse 3');

-- Создание и заполнение таблицы storehouses_products
DROP TABLE IF EXISTS storehouses_products;
CREATE TABLE storehouses_products (
  id SERIAL PRIMARY KEY,
  storehouse_id INT UNSIGNED,
  product_id INT UNSIGNED,
  value INT UNSIGNED COMMENT 'Запас товарной позиции на складе',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = 'Запасы на складе';

INSERT INTO storehouses_products
	(id, storehouse_id, product_id, value)
VALUES
	(NULL, 1, 3, 239),
	(NULL, 2, 1, 90),
	(NULL, 2, 7, 0),
	(NULL, 1, 4, 100),
	(NULL, 2, 3, 400),
	(NULL, 3, 1, 50),
	(NULL, 3, 2, 2500),
	(NULL, 1, 7, 5),
	(NULL, 1, 2, 0),
	(NULL, 2, 4, 10),
	(NULL, 3, 3, 0),
	(NULL, 1, 5, 0),
	(NULL, 2, 5, 888);

-- ------------------------------------------------------------------------------
-- Практическое задание по теме «Операторы, фильтрация, сортировка и ограничение»
-- ------------------------------------------------------------------------------

-- Задание 2
/* Таблица users была неудачно спроектирована. 
 * Записи created_at и updated_at были заданы типом VARCHAR и в них долгое время помещались значения в формате 20.10.2017 8:10. 
 * Необходимо преобразовать поля к типу DATETIME, сохранив введённые ранее значения.*/

SELECT * FROM users;
-- |id |name     |birthday_at|created_at     |updated_at     |
-- |---|---------|-----------|---------------|---------------|
-- |1  |Геннадий |1990-10-05 |20.10.2017 8:10|21.10.2017 8:10|
-- |2  |Наталья  |1984-11-12 |22.10.2017 8:10|23.10.2017 8:10|
-- |3  |Александр|1985-05-20 |24.10.2017 8:10|25.10.2017 8:10|
-- |4  |Сергей   |1988-02-14 |20.11.2017 8:10|21.11.2017 8:10|
-- |5  |Иван     |1998-01-12 |25.11.2017 8:10|26.10.2017 8:10|
-- |6  |Мария    |1992-08-29 |22.12.2017 8:10|24.12.2017 8:10|

-- при создании таблицы был специально указан тип данных VARCHAR created_at VARCHAR(50) NULL, updated_at VARCHAR(50) NULL
-- Решение: для выполнения задания вначале переведем даты из заданного формата в стандартный формат MySQL, далее изменим тип столбцов на DATETIME
UPDATE users SET updated_at = STR_TO_DATE(updated_at, '%d.%m.%Y %H:%i');
UPDATE users SET created_at = STR_TO_DATE(created_at, '%d.%m.%Y %H:%i');
ALTER TABLE users MODIFY created_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
ALTER TABLE users MODIFY updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

DESC users;
-- Field      |Type           |Null|Key|Default          |Extra                                        |
-- -----------|---------------|----|---|-----------------|---------------------------------------------|
-- id         |bigint unsigned|NO  |PRI|                 |auto_increment                               |
-- name       |varchar(255)   |YES |   |                 |                                             |
-- birthday_at|date           |YES |   |                 |                                             |
-- created_at |datetime       |YES |   |CURRENT_TIMESTAMP|DEFAULT_GENERATED on update CURRENT_TIMESTAMP|
-- updated_at |datetime       |YES |   |CURRENT_TIMESTAMP|DEFAULT_GENERATED on update CURRENT_TIMESTAMP|

SELECT * FROM users;
-- id|name     |birthday_at|created_at         |updated_at         |
-- --|---------|-----------|-------------------|-------------------|
--  1|Геннадий | 1990-10-05|2017-10-20 08:10:00|2017-10-21 08:10:00|
--  2|Наталья  | 1984-11-12|2017-10-22 08:10:00|2017-10-23 08:10:00|
--  3|Александр| 1985-05-20|2017-10-24 08:10:00|2017-10-25 08:10:00|
--  4|Сергей   | 1988-02-14|2017-11-20 08:10:00|2017-11-21 08:10:00|
--  5|Иван     | 1998-01-12|2017-11-25 08:10:00|2017-10-26 08:10:00|
--  6|Мария    | 1992-08-29|2017-12-22 08:10:00|2017-12-24 08:10:00|

-- Задание 3
/* В таблице складских запасов storehouses_products в поле value могут встречаться самые разные цифры: 0, если товар закончился 
 * и выше нуля, если на складе имеются запасы. Необходимо отсортировать записи таким образом, 
 * чтобы они выводились в порядке увеличения значения value. Однако нулевые запасы должны выводиться в конце, после всех записей.
 * Решение: сначала отсортируем столбец value по условию: если значение столбца 0, то вернем 0, в остальных случаях 1.
 * Таким образом получим столбец-маску, состоящий из нулей и единиц, который упорядочиваем в обратном порядке, чтобы нулевые значения
 * находились внизу, далее проводим сортировку по оригинальному столбцу в прямом порядке. В первой группе значения больше нуля, они идут первыми
 * и упорядочены внутри по оригинальному столбцу. Вторая группа состоит из нулей и из порядок не определен*/

SELECT value
  FROM storehouses_products
 ORDER BY CASE value 
 		  WHEN 0 THEN 0 
  		  ELSE 1 
   		  END DESC, value;

-- value|
-- -----|
--     5|
--    10|
--    50|
--    90|
--   100|
--   239|
--   400|
--   888|
--  2500|
--     0|
--     0|
--     0|
--     0|

-- Задание 4
/* (по желанию) Из таблицы users необходимо извлечь пользователей, родившихся в августе и мае. Месяцы заданы в виде списка английских названий (may, august)
 * Решение: используем функцию MONTHNAME, которая возвращает имя месяца даты-аргумента, и проверяем на вхождение в заданный список месяцев*/
   		 
SELECT * FROM users
 WHERE MONTHNAME(birthday_at) IN ('may', 'august');

-- id|name     |birthday_at|created_at         |updated_at         |
-- --|---------|-----------|-------------------|-------------------|
--  3|Александр| 1985-05-20|2017-10-24 08:10:00|2017-10-25 08:10:00|
--  6|Мария    | 1992-08-29|2017-12-22 08:10:00|2017-12-24 08:10:00|

-- Задание 5
/* (по желанию) Из таблицы catalogs извлекаются записи при помощи запроса SELECT * FROM catalogs WHERE id IN (5, 1, 2); 
 * Отсортируйте записи в порядке, заданном в списке IN.
 * Решение двумя способами
 * 1. через CASE, где формируем вручную порядок сортировки
 * 2. через функцию FIELD, которая возвращает индекс значения id в последовательности. Этот вариант запроса компактнее*/

SELECT * 
  FROM catalogs 
 WHERE id IN (5, 1, 2)
 ORDER BY CASE id
		  WHEN 5 THEN 1
		  WHEN 1 THEN 2
		  WHEN 2 THEN 3
		  END;

SELECT * 
  FROM catalogs 
 WHERE id IN (5, 1, 2)
 ORDER BY FIELD(id, 5, 1, 2);

-- id|name              |
-- --|------------------|
--  5|Оперативная память|
--  1|Процессоры        |
--  2|Материнские платы |

-- --------------------------------------------
-- Практическое задание теме «Агрегация данных»
-- --------------------------------------------

-- Задание 1
-- Подсчитайте средний возраст пользователей в таблице users.
SELECT name, TIMESTAMPDIFF(YEAR, birthday_at, NOW()) AS age
  FROM users;
 
-- name     |age|
-- ---------|---|
-- Геннадий | 30|
-- Наталья  | 36|
-- Александр| 35|
-- Сергей   | 33|
-- Иван     | 23|
-- Мария    | 28|

SELECT AVG(TIMESTAMPDIFF(YEAR, birthday_at, NOW())) AS avg_age
  FROM users;

-- avg_age|
-- -------|
-- 30.8333|

-- Задание 2
/* Подсчитайте количество дней рождения, которые приходятся на каждый из дней недели. 
 * Следует учесть, что необходимы дни недели текущего года, а не года рождения.
 * Задание выполнено с учетом дней рождения 29.02 */

SELECT DAYNAME(DATE_ADD(birthday_at, INTERVAL (YEAR(CURRENT_DATE()) - YEAR(birthday_at)) YEAR)) AS bday_name_up_to_date,
	   COUNT(*) AS cnt
  FROM users
  GROUP BY bday_name_up_to_date

-- bday_name_in_current_year|cnt|
-- -------------------------|---|
-- Tuesday                  |  2|
-- Friday                   |  1|
-- Thursday                 |  1|
-- Sunday                   |  2|

-- Задание 3
-- (по желанию) Подсчитайте произведение чисел в столбце таблицы.

SELECT EXP(SUM(LN(value))) AS m 
  FROM storehouses_products;
 
-- m                  |
-- -------------------|
-- 4775219999999991800|

/*WITH RECURSIVE cte (counter, n) AS
(
	SELECT 0 as counter, 1 AS n
	UNION ALL
	SELECT counter + 1, n * (SELECT value from storehouses_products limit 1 offset 0) from cte where counter <= 3
)
SELECT * FROM cte*/