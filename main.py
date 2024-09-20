from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import spacy
import re
import openai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

# --------------------------------------------------------------------------------------------------------------------


db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secrets"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///video-meeting.db"
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Register.query.get(int(user_id))


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True


with app.app_context():
    db.create_all()


class RegistrationForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    first_name = StringField(label="First Name", validators=[DataRequired()])
    last_name = StringField(label="Last Name", validators=[DataRequired()])
    username = StringField(label="Username", validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8, max=20)])


class LoginForm(FlaskForm):
    email = EmailField(label='Email', validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Register.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return render_template("index.html")

    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_user = Register(
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created Successfully! <br>You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# --------------------------------------------------------------------------------------------------------------------
openai.api_key = 'YOUR KEY'





@app.route('/chest')
def chest():
    return render_template('chest_x_ray.html')
@app.route('/blood')
def blood():
    return render_template('check_blood_report.html')
@app.route('/Homee')
def Homee():
    return render_template('index.html')

@app.route('/chatbottt')
def chetttt():
    return render_template('chatbott.html')

# ---------------------------------------------------------------------------------


masterr = ""
chat_count = 0



@app.route('/chat', methods=['POST'])
def chat():
    global masterr, chat_count
    user_input = request.json['user_input']
    if chat_count == 0:
        masterr = first_qu(user_input)
    elif chat_count == 1:
        masterr = secound_qu(user_input)
    elif chat_count == 2:
        masterr = three_qu(user_input)
    elif chat_count == 3:
        masterr = four_qu(user_input)
    elif chat_count == 4:
        masterr = five_qu(user_input)
    chat_count += 1
    return jsonify({'Provider': masterr})

def first_qu(user_input):
    global masterr
    First_Frist = "I have " + user_input + ". Ask 2 questions related to this health issue."
    response = chatmodel1(First_Frist)
    return response

def secound_qu(user_input):
    global masterr
    secound_fianl = masterr + " And " + user_input + "Ask 2 questions related to this health issue."
    response = chatmodel2(secound_fianl)
    return response

def three_qu(user_input):
    global masterr
    three_final = masterr + " And " + user_input + "Ask 2 questions related to this health issue."
    response = chatmodel3(three_final)
    return response

def four_qu(user_input):
    global masterr
    four_final = masterr + " And " + user_input + "Ask 2 questions related to this health issue."
    response = chatmodel4(four_final)
    return response

def five_qu(user_input):
    global masterr
    five_final = masterr + " And " + user_input + "for this i want 2 to 4 Evaluation points, 3 different diagnoses with biref   description and ICD10 Code, for all 3  diagnosis i want 3 diagnosis-test names, 3 names of treatment with CPT Codes, 2 medication details with 2 drug name  or 2 patient education"
    response = chatmodel5(five_final)
    return response

def chatmodel1(First_Frist):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": First_Frist}],
        temperature=0.1
    )
    generated_text = completion["choices"][0]["message"]["content"]
    # print(generated_text)
    generated_text_with_line_breaks = generated_text.replace('\n', '\\n')

    return generated_text_with_line_breaks

def chatmodel2(secound_qu):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": secound_qu}],
        temperature=0.1
    )
    generated_text = completion["choices"][0]["message"]["content"]
    generated_text_with_line_breaks = generated_text.replace('\n', '<br>')

    return generated_text_with_line_breaks

def chatmodel3(three_final):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": three_final}],
        temperature=0.1
    )
    generated_text = completion["choices"][0]["message"]["content"]
    generated_text_with_line_breaks = generated_text.replace('\n', '<br>')

    return generated_text_with_line_breaks

def chatmodel4(four_final):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": four_final}],
        temperature=0.1
    )
    generated_text = completion["choices"][0]["message"]["content"]
    generated_text_with_line_breaks = generated_text.replace('\n', '<br>')

    return generated_text_with_line_breaks

def chatmodel5(five_final):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": five_final}],
        temperature=0.1
    )
    generated_text = completion["choices"][0]["message"]["content"]
    generated_text_with_line_breaks = generated_text.replace('\n', '<br>')

    return generated_text_with_line_breaks


# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
