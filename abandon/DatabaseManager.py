import mysql.connector
from Snowflake import Snowflake
import os
from logger_config import get_logger

snowflake = Snowflake(worker_id=1, data_center_id=1)
logger = get_logger(__name__)
class DatabaseManager:
    def __init__(self):
        self.db_host=os.getenv('DB_HOST', '127.0.0.1')
        self.db_user=os.getenv('DB_USER', 'root')
        self.db_password=os.getenv('DB_PASSWORD', '2397947891')
        self.db_database=os.getenv('DB_NAME', 'student_db')
        self.mydb_connection = None
        self.get_connect()

    def get_connect(self):
        try:
            self.mydb_connection = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_database,
                #autocommit=True
            )
            if self.mydb_connection.is_connected():
                logger.info("数据库连接成功")
            else:
                try:
                    self.mydb_connection.reconnect(attempts=5, delay=5)
                    logger.info("数据库重连成功")
                except mysql.connector.Error as error:
                    logger.error(f"数据库连接失败: {error}")
        except mysql.connector.Error as error:
            logger.error(f"数据库连接失败: {error}")

    def get_cursor(self):
        if not self.mydb_connection.is_connected():
            self.get_connect()
        return self.mydb_connection.cursor()

mydb=DatabaseManager()
snowflake_id = snowflake.next_id()
person_cursor = mydb.get_cursor()
person_cursor.execute("CREATE TABLE if not exists persons (ID BIGINT not null PRIMARY KEY,"
                      "number VARCHAR(10) not null UNIQUE,"
                      "password VARCHAR(50) not null,"
                      "name varchar(255),"
                      "age int(3),"
                      "gender char(1),"
                      "role varchar(20) not null,"
                      "grade varchar(20),"
                      "position varchar(20))")

person_cursor.execute("CREATE OR REPLACE VIEW persons_root_view AS "  # OR REPLACE 再次执行：删除旧视图，创建新视图（不会报错）
                      "SELECT number, password, name, age, gender, role, grade, position FROM persons")  # 只返回部分列的视图语法

person_cursor.execute("CREATE OR REPLACE VIEW persons_user_view AS "
                      "SELECT number, name, age, gender, role, grade, position FROM persons")

person_cursor.execute("insert IGNORE into persons(ID, number, password, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                      (snowflake_id,'admin', 'admin123', 'Administrator', 1, 'M', 'root', None, None))
mydb.mydb_connection.commit()
person_cursor.close()


def person_add(user):
    try:
        person_add_cursor = mydb.get_cursor()
        snowflake_id = snowflake.next_id()
        person_add_cursor.execute("INSERT INTO persons (ID, number, password, name, age, gender, role, grade, position) "
                                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                  (snowflake_id, user.number, user.password, user.name, user.age, user.gender, user.role, user.grade,user.position))
        mydb.mydb_connection.commit()
        person_add_cursor.close()
        return True
    except mysql.connector.Error as error:
        return False


# person_delete_cursor.execute("DELETE students,teachers FROM students JOIN teachers on students.number=teachers.number where students.number = %s",(user_first_element,))

def person_delete(user):
    person_delete_cursor = mydb.get_cursor()
    try:
        person_delete_cursor.execute("DELETE FROM persons where number=%s", (user.number,))
        mydb.mydb_connection.commit()
        person_delete_cursor.close()
        return True
    except mysql.connector.Error as error:
        return False


def get_person_id(user):
    try:
        get_person_id_cursor = mydb.get_cursor()
        get_person_id_cursor.execute("SELECT ID FROM persons WHERE number = %s AND name = %s AND age = %s",
                                     (user.number, user.name, user.age))
        result_ID = get_person_id_cursor.fetchone()
        get_person_id_cursor.close()
        return result_ID[0]
    except mysql.connector.Error as error:
        return False


def person_update(user, get_id):
    try:
        person_update_cursor = mydb.get_cursor()
        person_update_cursor.execute("UPDATE persons SET number=%s, password=%s, name = %s, age=%s, gender=%s, role=%s, grade=%s, position=%s where ID = %s",
                                     (user.number, user.password, user.name, user.age, user.gender, user.role, user.grade,user.position, get_id))
        mydb.mydb_connection.commit()
        person_update_cursor.close()
        return True
    except mysql.connector.Error as error:
        return False


def person_find(field_type, find_value):
    person_find_cursor = mydb.get_cursor()
    person_find_cursor.execute(f"SELECT * FROM persons_root_view where {field_type} = %s AND number != 'admin'", (find_value,))
    result_find = person_find_cursor.fetchall()
    person_find_cursor.close()
    if result_find:
        return result_find
    else:
        return False


def all_person_root():
    all_person_cursor = mydb.get_cursor()
    all_person_cursor.execute("SELECT * FROM persons_root_view WHERE number != 'admin'")
    try:
        results_all = all_person_cursor.fetchall()
        all_person_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        return False

def all_person_user():
    all_person_cursor = mydb.get_cursor()
    all_person_cursor.execute("SELECT * FROM persons_user_view WHERE number != 'admin'")
    try:
        results_all = all_person_cursor.fetchall()
        all_person_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        return False

def verify_account(number, password):
    from User import User
    verify_account_cursor = mydb.get_cursor()
    verify_account_cursor.execute("SELECT * FROM persons_root_view where number = %s and password = %s", (number, password))
    result = verify_account_cursor.fetchone()
    if result:
        user=User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user
    else:
        return False

def register_account(user):
    try:
        register_account_cursor = mydb.get_cursor()
        snowflake_id = snowflake.next_id()
        register_account_cursor.execute("insert into persons(ID, number, password, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                        (snowflake_id, user.number, user.password, user.name, user.age, user.gender, user.role, user.grade, user.position))
        mydb.mydb_connection.commit()
        register_account_cursor.close()
        return True
    except mysql.connector.Error as error:
        return False