import bcrypt
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from UserGlobalVariables import *
from services.UserService import UserService


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class UserDBModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    food = db.Column(db.Integer, default=0, nullable=False)
    fun = db.Column(db.Integer, default=0, nullable=False)
    school = db.Column(db.Integer, default=0, nullable=False)
    personal = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, name, password, food=0, fun=0, school=0, personal=0):
        self.name = name
        self.password = password
        self.food = food
        self.fun = fun
        self.school = school
        self.personal = personal

    def __repr__(self):
        return f''' <User(id='{self.id}', name='{self.name}', password='{self.password}'
        food='{self.food}', fun='{self.fun}', school='{self.school}', personal='{self.personal}')>'''


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('login_register.html')

    elif request.method == 'POST':
        # save user data and check which button was clicked
        name = request.form.get('name')
        password = request.form.get('password')
        action = request.form.get('action')
        user = UserDBModel(name=name, password=password)

        if action == 'login':
            login_state = UserService().login_user(user, db)

            if login_state == LOGIN_SUCCES:
                return redirect(url_for('expenses', name=name))
            elif login_state == LOGIN_FAIL:
                return render_template('login_register.html', login_failed=True)
            elif login_state == USER_NOT_FOUND:
                return render_template('login_register.html', user_not_found=True)
            else:
                return "Unknown error"

        elif action == 'register':
            register_state = UserService().register_user(user, db)

            if register_state == REGISTER_SUCCESS:
                return redirect(url_for('expenses', name=name))
            elif register_state == USER_REGISTERED:
                return render_template('login_register.html', user_registered=True)
            elif register_state == REGISTER_FAIL:
                return "User registration failed!"
            else:
                return "Unknown error"
        else:
            return "Unknown action"
    else:
        return "Invalid request method"


@app.route('/expenses/<name>', methods=['GET', 'POST'])
def expenses(name):
    user = db.session.query(UserDBModel).filter_by(name=name).first()

    if request.method == 'GET':
        if user:
            return render_template('expenses_table.html', user=user)
        else:
            return "User not found", 404

    elif request.method == 'POST':
        action = request.form.get('action')
        if action == 'save':
            if user:
                user.food += int(request.form.get('food')) if request.form.get('food') != '' else 0
                user.fun += int(request.form.get('fun')) if request.form.get('fun') != '' else 0
                user.school += int(request.form.get('school')) if request.form.get('school') != '' else 0
                user.personal += int(request.form.get('personal')) if request.form.get('personal') != '' else 0
                db.session.commit()
                return render_template('expenses_table.html', user=user)
        elif action == 'reset':
            if user:
                user.food = user.fun = user.school = user.personal = 0
                db.session.commit()
                return render_template('expenses_table.html', user=user)
        else:
            return "User not found", 404



@app.route('/delete/<name>')
def deleteUser(name):
    user = db.session.query(UserDBModel).filter_by(name=name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main'))
    else:
        return "User not found", 404


@app.route('/delete')
def deleteAllUsers():
    users = db.session.query(UserDBModel).all()
    if users:
        for user in users:
            db.session.delete(user)
        db.session.commit()
        return redirect(url_for('main'))
    else:
        return "No users found"

@app.route('/favicon.ico')
def favicon():
    return ""


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True, port=5678)
