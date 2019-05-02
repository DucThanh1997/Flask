from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import pymysql
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'thanh1997'
app.config['MYSQL_DATABASE_DB'] = 'test1'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'



@app.route('/')
def index():

    return render_template('index.html')

@app.route('/show_login', methods = ['GET'])
def show_login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    # check xem điền đủ thông tin chưa
    name = request.form['username']
    password = request.form['password']
    if name and password:
        pass
    else:
        return json.dumps({'status': 'False', "messages":"Bạn chưa điền đủ dòng"})
    engine = create_engine('mysql://root:thanh1997@127.0.0.1')
    engine.execute("USE test1")
    user_list = engine.execute('select * from users')
    result = {'data': [dict(zip(tuple(user_list.keys()), i)) for i in user_list.cursor]}
    list1 = result['data']
    for x in list1:
        if x['username'] == name:
            if x['password'] == password:
                return json.dumps({'status': 'Done','messages':reverse('thành công')})
            else:
                return json.dumps({'status': 'False', "messages":"Sai mật khẩu"})
        else:
            pass
    return json.dumps({'status': 'False', "messages":"Sai tên người dùng"})

    # connect database
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="thanh191997",
                           db="test1")
    cursor = conn.cursor
    User_list = cursor.excute('select * from users')
    print(type(User_list))


@app.route('/show_sign_up')
def show_sign_up():
    return render_template('sign_up.html')

@app.route('/sign_up', methods = ['POST'])
def sign_up():
    name = request.form['inputName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']

    if name and email and password:
        return json.dumps({'html': '<span> okke </span>'})
    else:
        return json.dumps({'html': '<span> bạn chưa điền đủ </span>'})

    conn = mysql.connect
    cursor = conn.cursor
    hash_pass = generate_password_hash(password)
    cursor.callproc('sp_creatUser1', (name, email, hash_pass))
    data = cursor.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message':'User created successfully !'})
    else:
        return json.dumps({'error':str(data[0])})







if __name__ == "__main__":
    app.run()
