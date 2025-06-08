import mysql.connector
from Snowflake import Snowflake
import os

snowflake = Snowflake(worker_id=1, data_center_id=1)

"""
mydb = mysql.connector.connect(  # 数据库链接
    host="127.0.0.1"
    , user="root"
    , password="2397947891"
    , database="student_db"
)

"""
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST', '127.0.0.1'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD', '2397947891'),
    database=os.getenv('DB_NAME', 'student_db')
)

person_cursor = mydb.cursor()
person_cursor.execute("CREATE TABLE if not exists persons (ID BIGINT not null PRIMARY KEY,"
                      "number int(8) not null UNIQUE,"
                      "name varchar(255) not null,"
                      "age int(3) not null,"
                      "gender char(1) not null,"
                      "role varchar(20) not null,"
                      "grade varchar(20),"
                      "position varchar(20))")

person_cursor.execute("CREATE OR REPLACE VIEW persons_view AS "#OR REPLACE 再次执行：删除旧视图，创建新视图（不会报错）
                      "SELECT number, name, age, gender, role, grade, position FROM persons")#只返回部分列的视图语法

person_cursor.close()


def person_add(person):
    try:
        # class_name = person.__class__.__name__
        class_name = person.get_field_type()
        person_add_cursor = mydb.cursor()
        snowflake_id = snowflake.next_id()
        if class_name == "Student":
            person_add_cursor.execute(
                "INSERT INTO persons (ID, number, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                (snowflake_id, person.number, person.name, person.age, person.gender, person.role, person.grade, None))
        elif class_name == "Teacher":
            person_add_cursor.execute(
                "INSERT INTO persons (ID, number, name, age, gender, role, grade, position) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                (snowflake_id, person.number, person.name, person.age, person.gender, person.role, None,
                 person.position))
        else:
            person_add_cursor.close()
            return False
        mydb.commit()
        person_add_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
        return False


# person_delete_cursor.execute("DELETE students,teachers FROM students JOIN teachers on students.number=teachers.number where students.number = %s",(user_first_element,))

def person_delete(person):
    person_delete_cursor = mydb.cursor()
    # class_name=person.get_field_type()
    try:
        person_delete_cursor.execute("DELETE FROM persons where number=%s", (person.number,))
        mydb.commit()
        person_delete_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
        return False

def get_person_id(person):
    try:
        get_person_id_cursor = mydb.cursor()
        get_person_id_cursor.execute("SELECT ID FROM persons WHERE number = %s AND name = %s AND age = %s", (person.number,person.name,person.age))
        result_ID=get_person_id_cursor.fetchone()
        get_person_id_cursor.close()
        return result_ID[0]
    except mysql.connector.Error as error:
        print(error)
        return False

def person_update(person,get_id):
    try:
        person_update_cursor = mydb.cursor()
        class_name = person.get_field_type()
        if class_name == "Student":
            person_update_cursor.execute("UPDATE persons SET number=%s, name = %s, age=%s, gender=%s, role=%s, grade=%s, position=%s where ID = %s",
                                         (person.number,person.name,person.age,person.gender,person.role,person.grade, None,get_id))
        elif class_name =="Teacher":
            person_update_cursor.execute(
                "UPDATE persons SET number=%s, name = %s, age=%s, gender=%s, role=%s, grade=%s, position=%s where ID = %s",
                (person.number, person.name, person.age, person.gender, person.role, None, person.position,get_id))
        mydb.commit()
        person_update_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(error)
        return False


def person_find(field_type, find_value):
    person_find_cursor = mydb.cursor()
    if field_type == "grade":
        person_find_cursor.execute(f"SELECT * FROM persons_view where grade = %s", (find_value,))
    elif field_type == "position":
        person_find_cursor.execute(f"SELECT * FROM persons_view where position = %s", (find_value,))
    else:
        person_find_cursor.execute(f"SELECT * FROM persons_view where {field_type} = %s", (find_value,))
    result_find = person_find_cursor.fetchall()
    person_find_cursor.close()
    if result_find:
        return result_find
    else:
        return False


def all_person():  # 打印数据库内所有的
    all_person_cursor = mydb.cursor()
    all_person_cursor.execute("SELECT * FROM persons_view")
    try:
        results_all = all_person_cursor.fetchall()
        all_person_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")
        return False
