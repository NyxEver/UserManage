
import mysql.connector.pooling
from Snowflake import Snowflake
import os
from logger_config import get_logger

class DatabaseManagePooling:
    def __init__(self):
        self.db_pool = mysql.connector.pooling.MySQLConnectionPool(
            #pool_name='UserManage',
            pool_size=5,
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '2397947891'),
            database=os.getenv('DB_NAME', 'student_db')
        )

snowflake = Snowflake(worker_id=1, data_center_id=1)
logger = get_logger(__name__)
mydb=DatabaseManagePooling()
snowflake_id = snowflake.next_id()
pool_connection = mydb.db_pool.get_connection()
person_cursor = pool_connection.cursor()
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
pool_connection.commit()
person_cursor.close()
pool_connection.close()

def person_add(user):
    try:
        add_pool_connection = mydb.db_pool.get_connection()
        person_add_cursor = add_pool_connection.cursor()
        snowflake_id = snowflake.next_id()
        person_add_cursor.execute("INSERT INTO persons (ID, number, password, name, age, gender, role, grade, position) "
                                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                  (snowflake_id, user.number, user.password, user.name, user.age, user.gender, user.role, user.grade,user.position))
        add_pool_connection.commit()
        return True
    except mysql.connector.Error as error:
        return False
    finally:
        if person_add_cursor is not None:
            person_add_cursor.close()
        if add_pool_connection is not None:
            add_pool_connection.close()