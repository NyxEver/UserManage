import mysql.connector
from People import People

mydb = mysql.connector.connect(#数据库链接
    host="127.0.0.1"
    ,user="root"
    ,password="*"
    ,database="*"
)
print(mydb,"数据库连接成功!")

people_cursor = mydb.cursor()#创建游标
people_cursor.execute("CREATE TABLE if not exists people (number int(8) not null PRIMARY KEY,"#执行创建表的SQL语句
                       "name varchar(255) not null, age int(3) not null"
                       ",gender char(1) not null)")
people_cursor.close()#关闭游标
print("表 'people' 检查/创建 完成.")

def people_add(name, age, gender, number):#添加方法
    try:
        peopleAdd_cursor = mydb.cursor()
        peopleAdd_cursor.execute("INSERT INTO people(name,age,gender,number) values(%s,%s,%s,%s)",(name, age, gender, number))# 执行sql语句
        #peopleAdd_cursor.execute("INSERT INTO people (name, age, gender, number) values(%s,%s,%s,%s)",(person.name, person.age, person.gender, person.number))
        mydb.commit()# 提交到数据库执行
        print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: Name:{name}")
        #print(f"{peopleAdd_cursor.rowcount} 条记录插入成功: {person}")#print(person) 调用 __str__()
        peopleAdd_cursor.close()
        return True# 返回操作成功状态
    except mysql.connector.Error as error:
        print("出错内容：",error)
        return False# 返回操作失败状态

def people_delete(field_type , value):#删除方法，传入两个参数，1：类别，2：传入的参数
    people_delete_cursor = mydb.cursor()
    people_delete_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value,))#先寻找符合条件的记录
    if people_delete_cursor.fetchall():
        people_delete_cursor.execute(f"DELETE FROM people where {field_type} = %s",(value,))#确认删除符合条件的记录
        mydb.commit()
        return True
    else:
        print("取消删除成功")
        return False
    people_delete_cursor.close()

def people_change_dict(field_type,value_find,list_number):
    try:
        people_change_cursor = mydb.cursor()
        people_change_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value_find,))
        result_find = people_change_cursor.fetchall()
        if result_find:
            people_change_dict = dict(zip(['number', 'name', 'age', 'gender'], result_find[list_number]))
        else:
            return None
        #people_change_dict = dict(zip(['number', 'name', 'age', 'gender'], result_find[0]))
        print(people_change_dict)
        print("查询成功")
        people_change_cursor.close()
        return people_change_dict  # 返回字典而不是True
    except mysql.connector.Error as error:
        print(error)
        return None  # 失败时返回None

def change_value(people_change_dict,new_values):
    try:
        people_dict = people_change_dict.copy()
        people_dict['name']= new_values[0]
        people_dict['age']= new_values[1]
        people_dict['gender']= new_values[2]
        people_dict['number']= new_values[3]
        print("修改成功")
        return people_dict
    except Exception as e:
        print(f"修改失败: {e}")
        return None

def people_change(people_change_dict,people_dict):
    try:
        original_value= people_change_dict['number']
        new_value= people_dict['number']
        people_change_cursor = mydb.cursor()
        if original_value != new_value:
            people_change_cursor.execute(f"DELETE FROM people where number = %s",(original_value,))
            people_change_cursor.execute("INSERT INTO people (number, name, age, gender) VALUES (%s, %s, %s, %s)",
                                         (new_value, people_dict['name'], people_dict['age'], people_dict['gender']))
        else:
            people_change_cursor.execute(f"UPDATE people SET name = %s,age=%s,gender=%s where number = %s", (people_dict['name'], people_dict['age'], people_dict['gender'],original_value))
        mydb.commit()  # 提交
        print("修改成功")
        people_change_cursor.close()
        return True

    except mysql.connector.Error as error:
        print(error)
        return False

def people_find(field_type , value_1):
    people_find_cursor = mydb.cursor()
    people_find_cursor.execute(f"SELECT * FROM people where {field_type} = %s",(value_1,))
    result_find = people_find_cursor.fetchall()
    people_find_cursor.close()
    if result_find:
        #people_find_cursor.close()
        return result_find
    else:
        return False

def all_people():#打印数据库内所有的
    all_people_cursor = mydb.cursor()
    all_people_cursor.execute("SELECT * FROM people")#搜索people表内所有的数据
    try:
        results_all=all_people_cursor.fetchall()
        all_people_cursor.close()
        return results_all
    except mysql.connector.Error as error:
        print(f"ERROR:{error}")
        return False