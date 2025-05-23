from flask import Flask, render_template, request, redirect, url_for, abort
from SQL_People import people_add, people_delete, people_change, people_find, all_people, people_change_dict, \
    change_value
from SQL_account import verify_account,register_account

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/account_verify', methods=['POST'])
def account_verify():
    username = request.form['username']
    password = request.form['password']
    result_verify=verify_account(username,password)
    if result_verify:
        return redirect(url_for('welcome', username=username))
    else:
        return "账号或密码错误"

@app.route('/account_register', methods=['POST'])
def account_register():
    username = request.form['username']
    password = request.form['password' ]
    result_register = register_account(username,password)
    if result_register:
        return redirect(url_for('index', register_success='true', message="注册成功"))
    else:
        return "注册失败"

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

@app.route('/main')
def main():
    results_all = all_people()
    return render_template('main.html',results=results_all)

@app.route('/add_people', methods=['POST'])
def add_people():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    number = request.form['number']
    result_add = people_add(name, age, gender, number)
    if result_add: #检查 people_add() 返回的布尔值
        return redirect(url_for('main'))
    else:
        return "添加失败"

@app.route('/delete_people', methods=['POST'])
def delete_people():
    field_type = request.form['field_type']
    value = request.form['value']
    result_delete = people_delete(field_type, value)
    if result_delete:
        return redirect(url_for('main'))
    else:
        return "删除失败"

@app.route('/update_people', methods=['POST','GET'])
def update_people():
    field_type = request.form.get('field_type')
    value_find = request.form.get('value_1')
    list_number = request.form.get('list_number')
    if list_number is not None:
        try:
            list_number = int(list_number)
        except (ValueError, TypeError):
            return "列表索引无效"
    original_dict = people_change_dict(field_type, value_find, list_number)
    if not original_dict:
        return "未找到要修改的记录"
    new_values = [
        request.form.get('name', original_dict['name']),  # 如果未提供则使用原值
        int(request.form.get('age', original_dict['age'])),
        request.form.get('gender', original_dict['gender']),
        int(request.form.get('number', original_dict['number']))
    ]
    updated_dict = change_value(original_dict, new_values)
    result_update = people_change(original_dict,updated_dict)
    if result_update:
        return redirect(url_for('main'))
    else:
        return "修改失败"


@app.route('/find_people', methods=['POST'])
def find_people():
    field_type = request.form['field_type']
    value_1 = request.form['value_1']
    result_find = people_find(field_type, value_1)
    if result_find:
    #    return redirect(url_for('main'))
        return render_template('main.html', results=result_find, search_performed=True,
                              search_field=field_type, search_value=value_1)
    else:
        return render_template('main.html', results=[], search_performed=True, 
                              search_field=field_type, search_value=value_1)

app.run(debug = True)