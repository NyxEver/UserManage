import mysql.connector

mydb = mysql.connector.connect(#数据库链接
    host="127.0.0.1"
    ,user="root"
    ,password="*"
    ,database="*"
)

person_cursor = mydb.cursor()
person_cursor.execute("CREATE TABLE if not exists persons (number int(8) not null PRIMARY KEY,"
                      "name varchar(255) not null,"
                      "age int(3) not null,"
                      "gender char(1) not null,"
                      "role varchar(20) not null,"
                      "grade varchar(20),"
                      "position varchar(20))")
person_cursor.close()

def person_add(person):
    try:
        class_name = person.__class__.__name__
        person_add_cursor = mydb.cursor()
        if class_name == "Student":
            person_add_cursor.execute("INSERT INTO persons (number, name, age, gender, role,grade) values(%s,%s,%s,%s,%s,%s)",(person.number, person.name, person.age, person.gender, person.role, person.grade))
        elif class_name == "Teacher":
            person_add_cursor.execute("INSERT INTO persons (number, name, age, gender, role,position) values(%s,%s,%s,%s,%s,%s)",(person.number, person.name, person.age, person.gender, person.role, person.position))
        else:
            person_add_cursor.close()
            return False
        mydb.commit()
        person_add_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
        return False

#person_delete_cursor.execute("DELETE students,teachers FROM students JOIN teachers on students.number=teachers.number where students.number = %s",(user_first_element,))

def person_delete(person):
    person_delete_cursor = mydb.cursor()
    #class_name=person.get_field_type()
    try:
        person_delete_cursor.execute("DELETE FROM persons where number=%s",(person.number,))
        mydb.commit()
        person_delete_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
        return False

def person_update_dict(field_type,change_value,list_number):
    try:
        person_update_cursor = mydb.cursor()
        result_find= person_find(field_type,change_value)
        if result_find:
            if field_type == "grade":
                person_update_dict = dict(zip(['number', 'name', 'age', 'gender', 'grade'], result_find[list_number]))
            elif field_type == "position":
                person_update_dict = dict(zip(['number', 'name', 'age', 'gender', 'position'], result_find[list_number]))
        else:
            return None
        print(person_update_dict)
        person_update_cursor.close()
        return person_update_dict  # 返回字典而不是True
    except mysql.connector.Error as error:
        print(error)
        return None  # 失败时返回None

def update_value(person_update_dict,new_values):
    try:
        person_dict = person_update_dict.copy()
        person_dict['name']= new_values[0]
        person_dict['age']= new_values[1]
        person_dict['gender']= new_values[2]
        person_dict['number']= new_values[3]
        if 'grade' in person_dict:
            person_dict['grade']= new_values[4]
        elif 'position' in person_dict:
            person_dict['position']= new_values[4]
        print("修改成功")
        return person_dict
    except Exception as e:
        print(f"修改失败: {e}")
        return None
def person_update(person_change_dict,person_dict):
    try:
        original_value = person_change_dict['number']
        new_value = person_dict['number']
        person_change_cursor = mydb.cursor()
        if original_value != new_value:
            person_change_cursor.execute(f"DELETE students,teachers FROM students JOIN teachers on "
                                         f"students.number=teachers.number where student.number = %s",
                                         (original_value,))
            if 'grade' in person_dict:
                person_change_cursor.execute("INSERT INTO persons (number, name, age, gender,grade) VALUES (%s, %s, %s, %s, %s)",
                                             (new_value, person_dict['name'], person_dict['age'], person_dict['gender'], person_dict['grade']))
            elif 'position' in person_dict:
                person_change_cursor.execute("INSERT INTO persons (number, name, age, gender, position) VALUES (%s, %s, %s, %s, %s)",
                                             (new_value, person_dict['name'], person_dict['age'], person_dict['gender'], person_dict['position']))
        else:
            if 'grade' in person_dict:
                person_change_cursor.execute(f"UPDATE persons SET name = %s,age=%s,gender=%s, grade=%s where number = %s",
                                             (person_dict['name'], person_dict['age'], person_dict['gender'], person_dict['grade'], original_value))
            elif 'position' in person_dict:
                person_change_cursor.execute(f"UPDATE persons SET name = %s,age=%s,gender=%s, position=%s where number = %s",
                                             (person_dict['name'], person_dict['age'], person_dict['gender'],person_dict['position'], original_value))
        mydb.commit()
        print("修改成功")
        person_change_cursor.close()
        return True

    except mysql.connector.Error as error:
        print(error)
        return False
def person_find(field_type,find_value):
    person_find_cursor = mydb.cursor()
    if field_type == "grade":
        person_find_cursor.execute(f"SELECT * FROM persons where grade = %s", (find_value,))
    elif field_type == "position":
        person_find_cursor.execute(f"SELECT * FROM persons where position = %s", (find_value,))
    else:
        person_find_cursor.execute(f"SELECT * FROM persons where {field_type} = %s", (find_value,))
    result_find = person_find_cursor.fetchall()
    person_find_cursor.close()
    if result_find:
        return result_find
    else:
        return False
def all_person():#打印数据库内所有的
    all_person_cursor = mydb.cursor()
    all_person_cursor.execute("SELECT * FROM persons")#搜索people表内所有的数据
    try:
        results_all=all_person_cursor.fetchall()
        all_person_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")
        return False