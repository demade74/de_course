DROP DATABASE IF EXISTS example;
CREATE DATABASE example;

USE example;
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	name CHAR(20) DEFAULT 'anonymous' 
);
