-- �������� ��
CREATE DATABASE IF NOT EXISTS shop;
USE shop;

-- �������� � ���������� ������� catalogs
DROP TABLE IF EXISTS catalogs;
CREATE TABLE catalogs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT '�������� �������',
  UNIQUE unique_name(name(10))
) COMMENT = '������� ��������-��������';

INSERT INTO catalogs VALUES
  (NULL, '����������'),
  (NULL, '����������� �����'),
  (NULL, '����������'),
  (NULL, '������� �����'),
  (NULL, '����������� ������');

-- �������� � ���������� ������� users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT '��� ����������',
  birthday_at DATE COMMENT '���� ��������',
  created_at VARCHAR(50) NULL,
  updated_at VARCHAR(50) NULL
) COMMENT = '����������';

INSERT INTO users (name, birthday_at, created_at, updated_at) VALUES
  ('��������', '1990-10-05', '20.10.2017 8:10', '21.10.2017 8:10'),
  ('�������', '1984-11-12', '22.10.2017 8:10', '23.10.2017 8:10'),
  ('���������', '1985-05-20', '24.10.2017 8:10', '25.10.2017 8:10'),
  ('������', '1988-02-14', '20.11.2017 8:10', '21.11.2017 8:10'),
  ('����', '1998-01-12', '25.11.2017 8:10', '26.10.2017 8:10'),
  ('�����', '1992-08-29', '22.12.2017 8:10', '24.12.2017 8:10');

-- �������� � ���������� ������� products
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT '��������',
  description TEXT COMMENT '��������',
  price DECIMAL (11,2) COMMENT '����',
  catalog_id INT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_catalog_id (catalog_id)
) COMMENT = '�������� �������';

INSERT INTO products
  (name, description, price, catalog_id)
VALUES
  ('Intel Core i3-8100', '��������� ��� ���������� ������������ �����������, ���������� �� ��������� Intel.', 7890.00, 1),
  ('Intel Core i5-7400', '��������� ��� ���������� ������������ �����������, ���������� �� ��������� Intel.', 12700.00, 1),
  ('AMD FX-8320E', '��������� ��� ���������� ������������ �����������, ���������� �� ��������� AMD.', 4780.00, 1),
  ('AMD FX-8320', '��������� ��� ���������� ������������ �����������, ���������� �� ��������� AMD.', 7120.00, 1),
  ('ASUS ROG MAXIMUS X HERO', '����������� ����� ASUS ROG MAXIMUS X HERO, Z370, Socket 1151-V2, DDR4, ATX', 19310.00, 2),
  ('Gigabyte H310M S2H', '����������� ����� Gigabyte H310M S2H, H310, Socket 1151-V2, DDR4, mATX', 4790.00, 2),
  ('MSI B250M GAMING PRO', '����������� ����� MSI B250M GAMING PRO, B250, Socket 1151, DDR4, mATX', 5060.00, 2);

-- �������� � ���������� ������� orders
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  user_id INT UNSIGNED,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_user_id(user_id)
) COMMENT = '������';

-- �������� � ���������� ������� orders_products
DROP TABLE IF EXISTS orders_products;
CREATE TABLE orders_products (
  id SERIAL PRIMARY KEY,
  order_id INT UNSIGNED,
  product_id INT UNSIGNED,
  total INT UNSIGNED DEFAULT 1 COMMENT '���������� ���������� �������� �������',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = '������ ������';

-- �������� � ���������� ������� discounts
DROP TABLE IF EXISTS discounts;
CREATE TABLE discounts (
  id SERIAL PRIMARY KEY,
  user_id INT UNSIGNED,
  product_id INT UNSIGNED,
  discount FLOAT UNSIGNED COMMENT '�������� ������ �� 0.0 �� 1.0',
  started_at DATETIME,
  finished_at DATETIME,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY index_of_user_id(user_id),
  KEY index_of_product_id(product_id)
) COMMENT = '������';

-- �������� � ���������� ������� storehouses
DROP TABLE IF EXISTS storehouses;
CREATE TABLE storehouses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) COMMENT '��������',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = '������';

INSERT INTO storehouses 
	(id, name)
VALUES 
	(NULL, 'storehouse 1'),
	(NULL, 'storehouse 2'),
	(NULL, 'storehouse 3');

-- �������� � ���������� ������� storehouses_products
DROP TABLE IF EXISTS storehouses_products;
CREATE TABLE storehouses_products (
  id SERIAL PRIMARY KEY,
  storehouse_id INT UNSIGNED,
  product_id INT UNSIGNED,
  value INT UNSIGNED COMMENT '����� �������� ������� �� ������',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) COMMENT = '������ �� ������';

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
-- ������������ ������� �� ���� ����������, ����������, ���������� � �����������
-- ------------------------------------------------------------------------------

-- ������� 2
/* ������� users ���� �������� ��������������. 
 * ������ created_at � updated_at ���� ������ ����� VARCHAR � � ��� ������ ����� ���������� �������� � ������� 20.10.2017 8:10. 
 * ���������� ������������� ���� � ���� DATETIME, �������� �������� ����� ��������.*/

SELECT * FROM users;
-- |id |name     |birthday_at|created_at     |updated_at     |
-- |---|---------|-----------|---------------|---------------|
-- |1  |�������� |1990-10-05 |20.10.2017 8:10|21.10.2017 8:10|
-- |2  |�������  |1984-11-12 |22.10.2017 8:10|23.10.2017 8:10|
-- |3  |���������|1985-05-20 |24.10.2017 8:10|25.10.2017 8:10|
-- |4  |������   |1988-02-14 |20.11.2017 8:10|21.11.2017 8:10|
-- |5  |����     |1998-01-12 |25.11.2017 8:10|26.10.2017 8:10|
-- |6  |�����    |1992-08-29 |22.12.2017 8:10|24.12.2017 8:10|

-- ��� �������� ������� ��� ���������� ������ ��� ������ VARCHAR created_at VARCHAR(50) NULL, updated_at VARCHAR(50) NULL
-- �������: ��� ���������� ������� ������� ��������� ���� �� ��������� ������� � ����������� ������ MySQL, ����� ������� ��� �������� �� DATETIME
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
--  1|�������� | 1990-10-05|2017-10-20 08:10:00|2017-10-21 08:10:00|
--  2|�������  | 1984-11-12|2017-10-22 08:10:00|2017-10-23 08:10:00|
--  3|���������| 1985-05-20|2017-10-24 08:10:00|2017-10-25 08:10:00|
--  4|������   | 1988-02-14|2017-11-20 08:10:00|2017-11-21 08:10:00|
--  5|����     | 1998-01-12|2017-11-25 08:10:00|2017-10-26 08:10:00|
--  6|�����    | 1992-08-29|2017-12-22 08:10:00|2017-12-24 08:10:00|

-- ������� 3
/* � ������� ��������� ������� storehouses_products � ���� value ����� ����������� ����� ������ �����: 0, ���� ����� ���������� 
 * � ���� ����, ���� �� ������ ������� ������. ���������� ������������� ������ ����� �������, 
 * ����� ��� ���������� � ������� ���������� �������� value. ������ ������� ������ ������ ���������� � �����, ����� ���� �������.
 * �������: ������� ����������� ������� value �� �������: ���� �������� ������� 0, �� ������ 0, � ��������� ������� 1.
 * ����� ������� ������� �������-�����, ��������� �� ����� � ������, ������� ������������� � �������� �������, ����� ������� ��������
 * ���������� �����, ����� �������� ���������� �� ������������� ������� � ������ �������. � ������ ������ �������� ������ ����, ��� ���� �������
 * � ����������� ������ �� ������������� �������. ������ ������ ������� �� ����� � �� ������� �� ���������*/

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

-- ������� 4
/* (�� �������) �� ������� users ���������� ������� �������������, ���������� � ������� � ���. ������ ������ � ���� ������ ���������� �������� (may, august)
 * �������: ���������� ������� MONTHNAME, ������� ���������� ��� ������ ����-���������, � ��������� �� ��������� � �������� ������ �������*/
   		 
SELECT * FROM users
 WHERE MONTHNAME(birthday_at) IN ('may', 'august');

-- id|name     |birthday_at|created_at         |updated_at         |
-- --|---------|-----------|-------------------|-------------------|
--  3|���������| 1985-05-20|2017-10-24 08:10:00|2017-10-25 08:10:00|
--  6|�����    | 1992-08-29|2017-12-22 08:10:00|2017-12-24 08:10:00|

-- ������� 5
/* (�� �������) �� ������� catalogs ����������� ������ ��� ������ ������� SELECT * FROM catalogs WHERE id IN (5, 1, 2); 
 * ������������ ������ � �������, �������� � ������ IN.
 * ������� ����� ���������
 * 1. ����� CASE, ��� ��������� ������� ������� ����������
 * 2. ����� ������� FIELD, ������� ���������� ������ �������� id � ������������������. ���� ������� ������� ����������*/

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
--  5|����������� ������|
--  1|����������        |
--  2|����������� ����� |

-- --------------------------------------------
-- ������������ ������� ���� ���������� �������
-- --------------------------------------------

-- ������� 1
-- ����������� ������� ������� ������������� � ������� users.
SELECT name, TIMESTAMPDIFF(YEAR, birthday_at, NOW()) AS age
  FROM users;
 
-- name     |age|
-- ---------|---|
-- �������� | 30|
-- �������  | 36|
-- ���������| 35|
-- ������   | 33|
-- ����     | 23|
-- �����    | 28|

SELECT AVG(TIMESTAMPDIFF(YEAR, birthday_at, NOW())) AS avg_age
  FROM users;

-- avg_age|
-- -------|
-- 30.8333|

-- ������� 2
/* ����������� ���������� ���� ��������, ������� ���������� �� ������ �� ���� ������. 
 * ������� ������, ��� ���������� ��� ������ �������� ����, � �� ���� ��������.
 * ������� ��������� � ������ ���� �������� 29.02 */

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

-- ������� 3
-- (�� �������) ����������� ������������ ����� � ������� �������.

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