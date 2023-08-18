# website-env\Scripts\activate.bat
# set FLASK_ENV=development
# set FLASK_APP=app
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.exceptions import abort
import config

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = config.secret_key


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Please check this field")])
    phone_number = StringField("Telephone Number", validators=[DataRequired()])
    description_of_query = TextAreaField("What can we help you with?", validators=[DataRequired(),
        Length(-1, 600,"Please use less than 600 characters")])
    submit = SubmitField("Submit")


def plaintext_formatter(text_file_name):
    file = open('static/textFiles/' + text_file_name + '.txt', 'r')
    return file.read().replace('\n', '<br>')


@app.route('/')
def index():
    txt = plaintext_formatter('homepage')
    return render_template('index.html', txt=txt)


@app.route('/Domestic')
def domestic():
    txt = plaintext_formatter('domestic')
    return render_template('domestic_commercial_systems.html', txt=txt)


@app.route('/Commercial')
def commercial():
    txt = plaintext_formatter('commercial')
    return render_template('domestic_commercial_systems.html', txt=txt)


@app.route('/Systems')
def systems():
    txt = plaintext_formatter('systems')
    return render_template('domestic_commercial_systems.html', txt=txt)


@app.route('/ContactUs', methods=['GET', 'POST'])
def contact_us():
    name = None
    email = None
    phone_number = None
    description_of_query = None
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        description_of_query = form.description_of_query.data
        form.name.data = ""
        form.email.data = ""
        form.phone_number.data = ""
        form.description_of_query.data = ""
    return render_template('contact_us.html', name=name, email=email, phone_number=phone_number,
                           description_of_query=description_of_query, form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
