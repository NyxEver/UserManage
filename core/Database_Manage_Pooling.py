import mysql.connector.pooling
import os
from core.logger_config import get_logger
from core.Snowflake import Snowflake

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
    delete_pool_connection = mydb.get_connect()
    user_delete_cursor = delete_pool_connection.cursor()
    try:
        user_delete_cursor.execute("DELETE FROM persons where number=%s", (user.number,))
        delete_pool_connection.commit()
        return True
    except mysql.connector.Error as error:
        logger.error(f"删除操作失败: {error}")
        return False
    finally:
        if user_delete_cursor:
            user_delete_cursor.close()
        if delete_pool_connection:
            delete_pool_connection.close()

def get_user_id(user):
    try:
        get_id_pool_connection = mydb.get_connect()
        get_user_id_cursor = get_id_pool_connection.cursor()
        get_user_id_cursor.execute("SELECT ID FROM persons WHERE number = %s AND name = %s AND age = %s",
                                     (user.number, user.name, user.age))
        result_ID = get_user_id_cursor.fetchone()
        get_user_id_cursor.close()
        return result_ID[0]
    except mysql.connector.Error as error:
        logger.error(f"操作失败: {error}")
        return False
    finally:
        if get_user_id_cursor:
            get_user_id_cursor.close()
        if get_id_pool_connection:
            get_id_pool_connection.close()

def user_update(user, get_id):
    try:
        update_pool_connection = mydb.get_connect()
        user_update_cursor = update_pool_connection.cursor()
        user_update_cursor.execute("UPDATE persons SET number=%s, password=%s, name = %s, age=%s, gender=%s, role=%s, grade=%s, position=%s where ID = %s",
                                     (user.number, user.password, user.name, user.age, user.gender, user.role, user.grade,user.position, get_id))
        update_pool_connection.commit()
        return True
    except mysql.connector.Error as error:
        logger.error(f"修改操作失败: {error}")
        return False
    finally:
        if user_update_cursor:
            user_update_cursor.close()
        if update_pool_connection:
            update_pool_connection.close()

def user_find(field_type, find_value):
    try:
        find_pool_connection = mydb.get_connect()
        user_find_cursor = find_pool_connection.cursor()
        user_find_cursor.execute(f"SELECT * FROM persons_root_view where {field_type} = %s AND number != 'admin'", (find_value,))
        result_find = user_find_cursor.fetchall()
        return result_find
    except mysql.connector.Error as error:
        logger.error(f"修改操作失败: {error}")
        return False
    finally:
        if user_find_cursor:
            user_find_cursor.close()
        if find_pool_connection:
            find_pool_connection.close()

def all_user_root():
    try:
        root_pool_connection = mydb.get_connect()
        all_user_cursor = root_pool_connection.cursor()
        all_user_cursor.execute("SELECT * FROM persons_root_view WHERE number != 'admin'")
        results_all = all_user_cursor.fetchall()
        all_user_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        logger.error(f"操作失败: {error}")
        return False
    finally:
        if all_user_cursor:
            all_user_cursor.close()
        if root_pool_connection:
            root_pool_connection.close()

def all_user_user():
    try:
        user_pool_connection = mydb.get_connect()
        all_user_cursor = user_pool_connection.cursor()
        all_user_cursor.execute("SELECT * FROM persons_user_view WHERE number != 'admin'")
        results_all = all_user_cursor.fetchall()
        all_user_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        logger.error(f"操作失败: {error}")
        return False
    finally:
        if all_user_cursor:
            all_user_cursor.close()
        if user_pool_connection:
            user_pool_connection.close()

def verify_account(number, password):
    try:
        from core.User import User
        verify_account_pool_connection = mydb.get_connect()
        verify_account_cursor = verify_account_pool_connection.cursor()
        verify_account_cursor.execute("SELECT * FROM persons_root_view where number = %s and password = %s", (number, password))
        result = verify_account_cursor.fetchone()
        user=User(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
        return user
    except mysql.connector.Error as error:
        logger.error(f"操作失败: {error}")
        return False
    finally:
        if verify_account_cursor:
            verify_account_cursor.close()
        if verify_account_pool_connection:
            verify_account_pool_connection.close()

def register_account(user):
    try:
        register_account_pool_connection = mydb.get_connect()
        register_account_cursor = register_account_pool_connection.cursor()
        snowflake_id = snowflake.next_id()
        register_account_cursor.execute("insert into persons(ID, number, password, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                        (snowflake_id, user.number, user.password, user.name, user.age, user.gender, user.role, user.grade, user.position))
        register_account_pool_connection.commit()
        return True
    except mysql.connector.Error as error:
        logger.error(f"操作失败: {error}")
        return False
    finally:
        if register_account_cursor:
            register_account_cursor.close()
        if register_account_pool_connection:
            register_account_pool_connection.close()