# website-env\Scripts\activate.bat
# set FLASK_ENV=development
# set FLASK_APP=app
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

app = Flask(__name__)

app.debug = True


def plaintext_formatter(text_file_name):
    file = open('static/' + text_file_name + '.txt', 'r')
    return file.read().replace('\n', '<br>')


@app.route('/')
def index():
    return render_template('index.html')


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
