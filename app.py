from flask import Flask, render_template, request, redirect, url_for
from DatabaseManager import all_person
from SQL_account import verify_account, register_account

from Person import Person
from Student import Student
from Teacher import Teacher

print("2025.05.26")
print("管理系统")
print("SQL+FLASK+HTML storage version v0.4")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/account_verify', methods=['POST'])
def account_verify():
    username = request.form['username']
    password = request.form['password']
    result_verify = verify_account(username, password)
    if result_verify:
        return redirect(url_for('welcome', username=username))
    else:
        return "账号或密码错误"


@app.route('/account_register', methods=['POST'])
def account_register():
    username = request.form['username']
    password = request.form['password']
    result_register = register_account(username, password)
    if result_register:
        # return redirect(url_for('index', register_success='true', message="注册成功"))
        return redirect(url_for('index', message="注册成功"))
    else:
        return "注册失败"


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


@app.route('/main')
def main():
    results_all = all_person()
    return render_template('main.html', results=results_all)


@app.route('/add_people', methods=['POST'])
def add_people():
    try:
        number = request.form['number']
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        role = request.form['role']
        input_status = request.form['input_status']
        status_value = request.form['status_value']
        if input_status == 'grade':
            student = Student(number, name, age, gender, role, status_value)
            result_add = student.save_SQL()
        elif input_status == 'position':
            teacher = Teacher(number, name, age, gender, role, status_value)
            result_add = teacher.save_SQL()
        if result_add:
            return redirect(url_for('main'))
        else:
            return "添加失败"
    except ValueError as error:
        return f"输入数据格式错误：{error}"


@app.route('/delete_people', methods=['POST'])
def delete_people():
    field_type = request.form['field_type']
    del_value = request.form['value_1']
    list_number = request.form.get('list_number')
    person_find_data = Person.find_SQL(field_type,del_value)
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    if person_data[4]=='Student':
        person_obj = Student(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5])
    elif person_data[4]=='Teacher':
        person_obj = Teacher(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5])
    result_delete = person_obj.delete_SQL()
    if result_delete:
        return redirect(url_for('main'))
    else:
        return "未找到 or 删除失败"

@app.route('/update_people', methods=['POST'])
def update_people():
    field_type = request.form.get('field_type')
    value_find = request.form.get('value_1')
    person_find_data = Person.find_SQL(field_type, value_find)
    list_number = request.form.get('list_number')
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    if person_data[4]=='Student':
        original_person_obj = Student(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6])
    elif person_data[4]=='Teacher':
        original_person_obj = Teacher(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6])
    original_dict = dict(zip(['number', 'name', 'age', 'gender','role','grade','position'], person_data))
    if not original_dict:
        return "未找到要修改的记录"
    new_values_list = [
        int(request.form.get('number', original_dict['number'])),# 如果未提供则使用原值
        request.form.get('name', original_dict['name']),
        int(request.form.get('age', original_dict['age'])),
        request.form.get('gender', original_dict['gender']),
        request.form.get('role', original_dict['role']),
        request.form.get('grade', original_dict['grade']),
        request.form.get('position', original_dict['position']),
    ]
    if new_values_list[4] == 'Student':
        person_obj = Student(new_values_list[0], new_values_list[1], new_values_list[2], new_values_list[3], new_values_list[4],
                             new_values_list[5], new_values_list[6])
    elif new_values_list[4] == 'Teacher':
        person_obj = Teacher(new_values_list[0], new_values_list[1], new_values_list[2], new_values_list[3], new_values_list[4],
                             new_values_list[5], new_values_list[6])
    get_id=original_person_obj.get_person_ID()
    result_update= person_obj.update_SQL(get_id)
    if result_update:
        return redirect(url_for('main'))
    else:
        return "修改失败"


@app.route('/find_people', methods=['POST'])
def find_people():
    field_type = request.form['field_type']
    value_1 = request.form['value_1']
    result_find = Person.find_SQL(field_type, value_1)
    if result_find:
        #    return redirect(url_for('main'))
        return render_template('main.html', results=result_find, search_performed=True,
                               search_field=field_type, search_value=value_1)
    else:
        return render_template('main.html', results=[], search_performed=True,
                               search_field=field_type, search_value=value_1)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
