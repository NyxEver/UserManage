from flask import Flask, render_template, request, redirect, url_for, abort
from SQL_People import people_add, people_delete, people_change,people_find

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    return redirect(url_for('welcome', username=username))

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

@app.route('/main')
def main():
    return render_template('main.html')

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
        abort = "添加失败"

@app.route('/delete_people', methods=['POST'])
def delete_people():
    field_type = request.form['field_type']
    value = request.form['value']
    result_delete = people_delete(field_type, value)
    if result_delete:
        return redirect(url_for('main'))
    else:
        return "删除失败"

@app.route('/update_people', methods=['POST'])
def update_people():
    field_type = request.form['field_type']
    value_1 = request.form['value_1']
    value_2 = request.form['value_2']
    result_update =people_change(field_type, value_1, value_2)
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
        return redirect(url_for('main'))
    else:
        return "查找错误"

app.run()