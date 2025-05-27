import mysql.connector

mydb = mysql.connector.connect(#数据库链接
    host="127.0.0.1"
    ,user="root"
    ,password="2397947891"
    ,database="*"
)
student_cursor = mydb.cursor()
student_cursor.execute("CREATE TABLE if not exists students (number int(8) not null PRIMARY KEY,"
                      "name varchar(255) not null,"
                      "age int(3) not null,"
                      "gender char(1) not null,"
                      "grade varchar(50) not null)")
student_cursor.close()

teacher_cursor = mydb.cursor()
teacher_cursor.execute("CREATE TABLE if not exists teachers (number int(8) not null PRIMARY KEY,"
                      "name varchar(255) not null,"
                      "age int(3) not null,"
                      "gender char(1) not null,"
                      "position varchar(50) not null)")
teacher_cursor.close()

def person_add(person):
    try:
        class_name = person.__class__.__name__
        person_add_cursor = mydb.cursor()
        if class_name == "Student":
            person_add_cursor.execute("INSERT INTO people (name, age, gender, number,grade) values(%s,%s,%s,%s)",(person.name, person.age, person.gender, person.number, person.grade))
        elif class_name == "Teacher":
            person_add_cursor.execute("INSERT INTO people (name, age, gender, number,position) values(%s,%s,%s,%s)",(person.name, person.age, person.gender, person.number, person.position))
        else:
            person_add_cursor.close()
            return False
        mydb.commit()
        person_add_cursor.close()
        return True
    except mysql.connector.Error as error:
        print(f"数据库错误: {error}")
        return False
def person_delete(person):
    pass
def person_update(person):
    pass
def person_find(field_type,find_value):
    person_find_cursor = mydb.cursor()
    person_find_cursor.execute(f"SELECT * FROM * where {field_type} = %s", (find_value,))
    result_find = person_find_cursor.fetchall()
    person_find_cursor.close()
    if result_find:
        return result_find
    else:
        return False
