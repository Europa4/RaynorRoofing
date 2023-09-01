# website-env\Scripts\activate.bat
# set FLASK_ENV=development
# set FLASK_APP=app
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.exceptions import abort
import smtplib
from email.mime.text import MIMEText
import config
import json

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = config.secret_key


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email("Please check this field")])
    phone_number = StringField("Telephone Number", validators=[DataRequired()])
    description_of_query = TextAreaField("What can we help you with?", validators=[DataRequired(),
                                                                                   Length(-1, 1000,
                                                                                          "Please use less than 1000 characters")])
    submit = SubmitField("Submit")


class Image:
    path = ''
    alt = ''
    caption = ''

    def __init__(self, path, alt, caption):
        self.path = path
        self.alt = alt
        self.caption = caption


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
    images = [Image('Domestic/Domestic1.jpeg', 'A new domestic roof', 'Need to add a description'),
              Image('Domestic/Domestic2.jpeg', 'A new domestic roof', 'Need to add a description'),
              Image('Domestic/Domestic3.jpeg', 'A new domestic roof', 'Need to add a description')]
    return render_template('domestic_commercial_systems.html', txt=txt, images=images)


@app.route('/Commercial')
def commercial():
    txt = plaintext_formatter('commercial')
    images = [Image('Domestic/Domestic1.jpeg', 'A new commercial roof', 'Need to add a description'),
              Image('Domestic/Domestic2.jpeg', 'A new commercial roof', 'Need to add a description'),
              Image('Domestic/Domestic3.jpeg', 'A new commercial roof', 'Need to add a description')]
    return render_template('domestic_commercial_systems.html', txt=txt, images=images)


@app.route('/Systems')
def systems():
    txt = plaintext_formatter('systems')
    images = [Image('Systems/roofing-system.jpg', '', 'High Performance Felt Roofing Systems'),
              Image('Systems/roofing-system1.jpg', '', 'High Performance Applied Liquid Roofing Systems'),
              Image('Systems/roofing-system2.jpg', '', 'High Performance Single-Ply Roofing Systems'),
              Image('Systems/roofing-system3.jpg', '', 'High Performance Mastic Asphalt Damp proofing.')]
    return render_template('domestic_commercial_systems.html', txt=txt, images=images)


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
        body = name + " has requested a callback on " + phone_number + " or " + email + " about \n" + description_of_query
        msg = MIMEText(body)
        msg['Subject'] = 'Callback request by ' + name
        msg['From'] = 'raynorroofingwebserver@gmail.com'
        msg['To'] = ', '.join(['simonjwoodward5@gmail.com'])
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login('raynorroofingwebserver@gmail.com', config.gmail_password)
            smtp_server.sendmail('raynorroofingwebserver@gmail.com', ['simonjwoodward5@gmail.com'], msg.as_string())
    return render_template('contact_us.html', name=name, email=email, phone_number=phone_number,
                           description_of_query=description_of_query, form=form)


@app.route('/Gallery')
def gallery():
    file = open('static/JsonFiles/Gallery.json')
    data = json.load(file)
    file.close()
    for galleryItem in data['GalleryEntries']:
        if galleryItem['Chirality'] == 'Left':
            galleryItem.update({'FirstDiv': 'col-md-7'})
            galleryItem.update({'SecondDiv': 'col-md-4'})
        else:
            galleryItem.update({'FirstDiv': 'col-md-7 order-md-2'})
            galleryItem.update({'SecondDiv': 'col-md-5 order-md-1'})
    return render_template('gallery.html', data=data)


@app.route('/Certifications')
def certifications():
    return render_template('base.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
