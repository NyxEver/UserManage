import mysql.connector.pooling
from Snowflake import Snowflake
import os
from logger_config import get_logger

class DatabaseManagePooling:
    def __init__(self):
        self.db_pool = self.create_pool()
    def create_pool(self):
        return mysql.connector.pooling.MySQLConnectionPool(
            # pool_name='UserManage',
            pool_size=5,
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '2397947891'),
            database=os.getenv('DB_NAME', 'student_db')
        )
    def get_connect(self):
        try:
            test_connect = self.db_pool.get_connection()
            if not test_connect.is_connected():
                test_connect.reconnect(attempts=5, delay=5)
                return test_connect
        except mysql.connector.Error as error:
            logger.error(f"数据库连接失败：{error}")

snowflake = Snowflake(worker_id=1, data_center_id=1)
logger = get_logger(__name__)
mydb=DatabaseManagePooling()
snowflake_id = snowflake.next_id()

pool_connection = mydb.db_pool.get_connection()
user_cursor = pool_connection.cursor()
user_cursor.execute("CREATE TABLE if not exists persons (ID BIGINT not null PRIMARY KEY,"
                      "number VARCHAR(10) not null UNIQUE,"
                      "password VARCHAR(50) not null,"
                      "name varchar(255),"
                      "age int(3),"
                      "gender char(1),"
                      "role varchar(20) not null,"
                      "grade varchar(20),"
                      "position varchar(20))")

user_cursor.execute("CREATE OR REPLACE VIEW persons_root_view AS "  # OR REPLACE 再次执行：删除旧视图，创建新视图（不会报错）
                      "SELECT number, password, name, age, gender, role, grade, position FROM persons")  # 只返回部分列的视图语法

user_cursor.execute("CREATE OR REPLACE VIEW persons_user_view AS "
                      "SELECT number, name, age, gender, role, grade, position FROM persons")

user_cursor.execute("insert IGNORE into persons(ID, number, password, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                      (snowflake_id,'admin', 'admin123', 'Administrator', 1, 'M', 'root', None, None))
pool_connection.commit()
user_cursor.close()
pool_connection.close()

def user_add(user):
    try:
        add_pool_connection = mydb.get_connect()
        user_add_cursor = add_pool_connection.cursor()
        snowflake_id = snowflake.next_id()
        user_add_cursor.execute("INSERT INTO persons (ID, number, password, name, age, gender, role, grade, position) "
                                  "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                  (snowflake_id, user.number, user.password, user.name, user.age, user.gender, user.role, user.grade,user.position))
        add_pool_connection.commit()
        return True
    except mysql.connector.Error as error:
        logger.error(f"添加操作失败: {error}")
        return False
    finally:
        if user_add_cursor:
            user_add_cursor.close()
        if add_pool_connection:
            add_pool_connection.close()

def user_delete(user):
    delete_pool_connection = mydb.mydb.get_connect()
    user_delete_cursor = delete_pool_connection.cursor()
    try:
        user_delete_cursor.execute("DELETE FROM persons where number=%s", (user.number,))
        mydb.mydb_connection.commit()
        return True
    except mysql.connector.Error as error:
        logger.error(f"删除操作失败: {error}")
        return False
    finally:
        if user_delete_cursor:
            user_delete_cursor.close()
        if delete_pool_connection:
            delete_pool_connection.close()