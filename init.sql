-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

-- 创建账户表
CREATE TABLE IF NOT EXISTS account (
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    identify CHAR(1) NOT NULL
);

-- 创建人员表
CREATE TABLE IF NOT EXISTS persons (
    ID BIGINT NOT NULL PRIMARY KEY,
    number INT(8) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    age INT(3) NOT NULL,
    gender CHAR(1) NOT NULL,
    role VARCHAR(20) NOT NULL,
    grade VARCHAR(20),
    position VARCHAR(20)
);
