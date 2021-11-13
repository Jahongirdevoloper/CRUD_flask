from flask import Flask, redirect, render_template, url_for, request, flash
from db import Db
from psycopg2._psycopg import Error

app = Flask(__name__)

@app.route('/')
def index():
    with Db() as corsur:
        corsur.execute(
            'select * from crud_data;'
        )
        all_data = corsur.fetchall()
    return render_template('index.html', employees=all_data)

@app.route('/add', methods=["GET", "POST"])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            with Db() as cursor:
                cursor.execute(
                    '''insert into crud_data(name, email, phone) values(%s,%s,%s)''',(name, email, str(phone))
                )
            return redirect(url_for('index'))
        except (Exception, Error) as e:
            print(e)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == "GET":
        with Db() as cursor:
            cursor.execute('select * from crud_data where id=%s',(id,))
            data = cursor.fetchone()
        return render_template('edit.html', employee=data)
    elif request.method == 'POST':
        id = int(id)
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        with Db() as cursor:
            cursor.execute(
                '''update crud_data 
                        set name=%s,email=%s,phone=%s
                            where id=%s''',(name,email,str(phone),id)
            )
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    if request.method == "GET":
        with Db() as cursor:
            cursor.execute(
                '''delete from crud_data where id=%s''',(id,)
            )
        return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)