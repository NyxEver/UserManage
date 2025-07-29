# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import paramiko
from datetime import datetime
import secrets
from functools import wraps
from core.logger_config import get_logger
from core.Database_Manage_Pooling import all_user_root, all_user_user
from core.User_Template import User_Template
from core.User import User

logger = get_logger(__name__)
print("2025.07.15")
print("管理系统")
print("SQL+FLASK+HTML storage version v0.6")

app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")
start_time = datetime.now()
keys=secrets.token_hex(16)
app.secret_key = (keys)

def require_role(require_role):#表示需要的最低权限角色
    def decorator(original_function):
        @wraps(original_function)
        def wrapper():
            if 'role' not in session:
                return render_template('index.html')
            if session['role'] == require_role:
                return original_function()
            else:
                return render_template('user_error.html')
        return wrapper
    return decorator


@app. route('/')
def index():
    return render_template('index.html')

@app.route('/account_verify', methods=['POST'])
def account_verify():
    number = request.form['username']
    password = request.form['password']
    result_verify = User_Template.verify_user_account(number, password)
    if result_verify:
        logger.info(number)
        session['username'] = number
        session['role'] = result_verify.role
        return redirect(url_for('welcome', username=number))
    else:
        return "账号或密码错误"


@app.route('/account_register', methods=['POST'])
def account_register():
    number = request.form['username']
    password = request.form['password']
    user=User(number, password,'name',1,'M', 'user', None, None)
    result_register = User_Template.register_account(user)
    if result_register:
        return redirect(url_for('index', message="注册成功"))
    else:
        return "注册失败"


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


@app.route('/main')
def main():
    try:
        if session['role'] == 'root':
            results_all = all_user_root()
        else:
            results_all = all_user_user()
        current_time = datetime.now()
        runtime = current_time - start_time
        days = runtime.days
        hours = runtime.seconds // 3600
        minutes = (runtime.seconds % 3600) // 60
        seconds = (runtime.seconds % 3600) % 60
        str_runtime = "%d天 %d小时 %d分钟 %d秒" % (days, hours, minutes, seconds)
        return render_template('main.html', results=results_all, runtime=str_runtime)
    except Exception as error:
        logger.error(error)


@app.route('/add_people', methods=['POST'])
@require_role('root')
def add_people():
    number = request.form['number']
    # password = request.form['password']
    password = request.form.get('password', 'default123')
    name = request.form['name']
    age = int(request.form['age'])
    gender = request.form['gender']
    role = request.form['role']
    grade = request.form['grade']
    position = request.form['position']
    user = User(number, password, name, age, gender, role, grade, position)
    result_add = user.save_SQL()
    if result_add:
        return redirect(url_for('main'))
    else:
        return "添加失败"
        logger.DEBUG(result_add)


@app.route('/delete_people', methods=['POST'])
@require_role('root')
def delete_people():
    field_type = request.form['field_type']
    del_value = request.form['value_1']
    list_number = request.form.get('list_number')
    person_find_data = User_Template.find_SQL(field_type,del_value)
    if not person_find_data:
        return "未找到符合条件的记录"
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    person_obj = User(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6], person_data[7])
    result_delete = person_obj.delete_SQL()
    if result_delete:
        return redirect(url_for('main'))
    else:
        return "未找到 or 删除失败"

@app.route('/update_people', methods=['POST'])
@require_role('root')
def update_people():
    field_type = request.form.get('field_type')
    value_find = request.form.get('value_1')
    person_find_data = User_Template.find_SQL(field_type, value_find)
    if not person_find_data:
        return "未找到符合条件的记录"
        logger.DEBUG(person_find_data)
    list_number = request.form.get('list_number')
    list_number = int(list_number)
    person_data = person_find_data[list_number]
    original_person_obj = User(person_data[0], person_data[1], person_data[2], person_data[3], person_data[4], person_data[5], person_data[6], person_data[7])
    original_dict = dict(zip(['number','password', 'name', 'age', 'gender','role','grade','position'], person_data))
    if not original_dict:
        return "未找到要修改的记录"
        logger.DEBUG(original_dict)
    new_values_list = [
        request.form.get('number', original_dict['number']),# 如果未提供则使用原值
        request.form.get('password', original_dict['password']),
        request.form.get('name', original_dict['name']),
        int(request.form.get('age', original_dict['age'])),
        request.form.get('gender', original_dict['gender']),
        request.form.get('role', original_dict['role']),
        request.form.get('grade', original_dict['grade']),
        request.form.get('position', original_dict['position']),
    ]
    person_obj = User(new_values_list[0], new_values_list[1], new_values_list[2], new_values_list[3], new_values_list[4],
                         new_values_list[5], new_values_list[6],new_values_list[7])
    get_id=original_person_obj.get_user_ID()
    result_update= person_obj.update_SQL(get_id)
    if result_update:
        return redirect(url_for('main'))
    else:
        return "修改失败"


@app.route('/find_people', methods=['POST'])
def find_people():
    field_type = request.form['field_type']
    value_1 = request.form['value_1']
    result_find = User_Template.find_SQL(field_type, value_1)
    if result_find:
        #    return redirect(url_for('main'))
        return render_template('main.html', results=result_find, search_performed=True,
                               search_field=field_type, search_value=value_1)
    else:
        return render_template('main.html', results=[], search_performed=True,
                               search_field=field_type, search_value=value_1)

ssh_connections = {}
@app.route('/terminal')
@require_role('root')
def terminal():
    return render_template('terminal.html')

@socketio.on('connect')
def handle_connect():
    print('客户端已连接')
    emit('status', {'message': '连接成功，请输入SSH连接信息'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开连接')
    # 清理SSH连接
    session_id = request.sid
    if session_id in ssh_connections:
        ssh_connections[session_id].close()
        del ssh_connections[session_id]


@socketio.on('ssh_connect')
def handle_ssh_connect(ssh_data):
    try:
        hostname = ssh_data['hostname']
        username = ssh_data['username']
        password = ssh_data['password']
        #port = ssh_data.get('port', 22)
        port = 22
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)
        session_id = request.sid
        ssh_connections[session_id] = ssh
        emit('ssh_connected', {'msg': f'成功连接到 {hostname}'})
    except Exception as error:
        emit('ssh_error', {'error': str(error)})


@socketio.on('execute_command')
def handle_execute_command(command_data):
    session_id = request.sid
    if session_id in ssh_connections:
        try:
            command = command_data['command']
            ssh = ssh_connections[session_id]

            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            exit_status = stdout.channel.recv_exit_status()

            emit('command_result', {
                'command': command,
                'output': output,
                'error': error,
                'exit_status': exit_status
            })
        except Exception as error:
            emit('command_error', {'error': str(error)})
    else:
        emit('command_error', {'error': '未建立SSH连接'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
