import os
from flask import Flask, url_for, jsonify, request, redirect, flash
import psycopg2
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from flask_login import LoginManager
from datetime import datetime
from wtforms import ValidationError
import scrap
from flask import render_template
import time
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from forms import RegistrationForm, LoginForm, EmailForm


app = Flask(__name__)

configuration = os.path.join(os.getcwd(), 'config.py')
app.config.from_pyfile(configuration)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)


@app.route('/home')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/vostok',methods=['POST', 'GET'])
def vostok():
    lst_bv = scrap.news("blizhnij-vostok/")
    return render_template('vostok.html', lst = lst_bv)

@app.route('/mnews',methods=['POST', 'GET'])
def mnews():
    lst_bv = scrap.news2()
    return render_template('mnews.html', lst = lst_bv)


@app.route('/news')
@login_required
def news():
    return render_template('news.html')

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('do_the_login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    email = User.query.filter_by(user_email=form.email.data).first()
    if email:
        raise ValidationError('Email Already Exists')
    if current_user.is_authenticated:
        flash('you are already registered')
        return redirect(url_for('home'))
    if form.validate_on_submit():
        User.create_user(
        user=form.name.data,
        email=form.email.data,
        password=form.password.data)
        flash('Registration Successful')
        return redirect(url_for('do_the_login'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def do_the_login():
    if current_user.is_authenticated:
        flash('you are already logged-in')
        return redirect(url_for('news'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid Credentials, Please try again')
            return redirect(url_for('do_the_login'))
        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('home'))

    return render_template('login.html', form=form)

@app.route('/contact',methods=['GET', 'POST'])
def contact():

    form = EmailForm()

    if form.validate_on_submit():
        flash('Your message sent, thank you')
        form.email.data = ''
        form.message.data = ''
        return render_template('contact.html', form=form)
    else:
        flash('check your email address')
        form.email.data = ''
        form.message.data = ''
        return render_template('contact.html', form=form)
    return render_template('contact.html', form=form)

@app.route('/slow')
def slow():
    import time
    time.sleep(5)
    return jsonify("oh so slow")

@app.route('/progress')
def progress():
    return render_template('progress.html')

@app.route('/progress2')
def progress2():
    return render_template('progress2.html')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    user_email = db.Column(db.String(60), unique=True, index=True)
    user_password = db.Column(db.String(80))
    registration_date = db.Column(db.DateTime, default=datetime.now)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    @classmethod
    def create_user(cls, user, email, password):
        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return user

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
@login_required
def log_out_user():
    logout_user()
    flash('Logged out Successfully')
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':

    db.create_all()

    app.run(debug=True)