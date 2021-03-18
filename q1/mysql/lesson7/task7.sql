INSERT orders (user_id) VALUES (5), (6), (5), (3), (1), (1), (4), (5), (1), (6);

-- Задание 1
-- Составьте список пользователей users, которые осуществили хотя бы один заказ orders в интернет магазине

SELECT DISTINCT u.name
  FROM users u
  JOIN orders o
    ON u.id = o.user_id;
    
-- name     |
-- ---------|
-- Геннадий |
-- Александр|
-- Сергей   |
-- Иван     |
-- Мария    |

-- Считаю, что inner join соединения достаточно, так как сам факт того, что пользователь попал в результат запроса,
-- говорит о том, что он осуществил хотя бы один заказ. Для исключения дублей вставил distinct
    
-- Задание 2
-- Выведите список товаров products и разделов catalogs, который соответствует товару
    
SELECT p.name, p.description, p.price, c.name AS `catalog`
  FROM products p
  JOIN catalogs c
    ON p.catalog_id = c.id;
    
-- name                   |description                                                                      |price   |catalog          |
-- -----------------------|---------------------------------------------------------------------------------|--------|-----------------|
-- Intel Core i3-8100     |Процессор для настольных персональных компьютеров, основанных на платформе Intel.| 7890.00|Процессоры       |
-- Intel Core i5-7400     |Процессор для настольных персональных компьютеров, основанных на платформе Intel.|12700.00|Процессоры       |
-- AMD FX-8320E           |Процессор для настольных персональных компьютеров, основанных на платформе AMD.  | 4780.00|Процессоры       |
-- AMD FX-8320            |Процессор для настольных персональных компьютеров, основанных на платформе AMD.  | 7120.00|Процессоры       |
-- ASUS ROG MAXIMUS X HERO|Материнская плата ASUS ROG MAXIMUS X HERO, Z370, Socket 1151-V2, DDR4, ATX       |19310.00|Материнские платы|
-- Gigabyte H310M S2H     |Материнская плата Gigabyte H310M S2H, H310, Socket 1151-V2, DDR4, mATX           | 4790.00|Материнские платы|
-- MSI B250M GAMING PRO   |Материнская плата MSI B250M GAMING PRO, B250, Socket 1151, DDR4, mATX            | 5060.00|Материнские платы|
    
-- Задание 3
-- (по желанию) Пусть имеется таблица рейсов flights (id, from, to) и таблица городов cities (label, name). 
-- Поля from, to и label содержат английские названия городов, поле name — русское. 
-- Выведите список рейсов flights с русскими названиями городов.
    
CREATE TABLE flights (
	id INT NOT NULL PRIMARY KEY,
	`from` VARCHAR(20) NOT NULL,
	`to` VARCHAR(20) NOT NULL
)

INSERT INTO flights
	(id, `from`, `to`)
VALUES
	(1, 'moscow', 'omsk'),
	(2, 'novgorod', 'kazan'),
	(3, 'irkutsk', 'moscow'),
	(4, 'omsk', 'irkutsk'),
	(5, 'moscow', 'kazan')
	
CREATE TABLE cities (
	label VARCHAR(20) NOT NULL,
	name VARCHAR(20) NOT NULL
)

INSERT INTO cities
	(label, name)
VALUES
	('moscow', 'Москва'),
	('irkutsk', 'Иркутск'),
	('novgorod', 'Новгород'),
	('kazan', 'Казань'),
	('omsk', 'Омск')
	
SELECT id, c1.name AS `from`, c2.name AS `to`
  FROM flights AS f1
  JOIN cities c1 
    ON f1.`from` = c1.label
  JOIN cities c2
  	ON f1.`to` = c2.label;
  
-- id|from    |to     |
-- --|--------|-------|
--  3|Иркутск |Москва |
--  4|Омск    |Иркутск|
--  2|Новгород|Казань |
--  5|Москва  |Казань |
--  1|Москва  |Омск   |
  