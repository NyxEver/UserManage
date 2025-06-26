-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS user_db;
USE user_db;

-- 创建人员表
CREATE TABLE IF NOT EXISTS persons (
    ID BIGINT NOT NULL PRIMARY KEY,
    number INT(8) NOT NULL UNIQUE,
    password VARCHAR(50) not null,
    name VARCHAR(255) NOT NULL,
    age INT(3) NOT NULL,
    gender CHAR(1) NOT NULL,
    role VARCHAR(20) NOT NULL,
    grade VARCHAR(20),
    position VARCHAR(20)
);
