from flask import Flask, render_template, url_for, session, flash, redirect
import os
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import (StringField, SelectField,
                     TextAreaField, SubmitField, validators)
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretKey'

# SQL DATABASE AND MODEL
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)


class Contact(db.Model):
    __tablename__ = 'Contant_Details'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text(120))
    message = db.Column(db.Text(2000))

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return f"Message From: {self.name}|{self.email} |Message: {self.message}"


class InfoForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=35)])
    message = TextAreaField('Message')
    submit = SubmitField('submit')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = InfoForm()
    name = form.name.data
    email = form.email.data
    message = form.message.data

    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['message'] = form.message.data

        new_mess = Contact(name, email, message)
        db.session.add(new_mess)
        db.session.commit()

        flash("Thank you we'll get back to you")

        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)


@app.route('/admin')
def admin():
    Contant_Details = Contact.query.all()
    return render_template('admin.html', Contant_Details=Contant_Details)


if __name__ == "__main__":
    app.run(debug=True)
