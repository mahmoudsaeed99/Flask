# -*- coding: utf-8 -*-
"""
Created on Mon May  8 21:35:18 2023

@author: Mahmoud Saeed
"""

from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo



# class RegistrationForm(FlaskForm):
#     username = StringField('UserName' ,
#                            validators=[DataRequired(),Length(min = 2 , max = 20)])
#     email = StringField('Email',
#                         validators = [DataRequired(),Email()])
#     password = PasswordField('password',
#                              validators = [DataRequired()])
    
#     confirm_password = PasswordField('confirm_password',
#                              validators = [DataRequired(),EqualTo('password')])
    

#     submit = SubmitField('sign up')

class LoginForm(FlaskForm):
    username = StringField('UserName' ,
                           validators=[DataRequired(),Length(min = 2 , max = 20)])
    password = PasswordField('password',
                             validators = [DataRequired()])
    remember = BooleanField('Remember me') 
    

    submit = SubmitField('Login')
    

from flask import Flask , render_template
import json

# from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/login')
def register():
    form = LoginForm()
    return render_template('login.html', form = form)
    


if __name__ == "__main__":
    app.run(debug = True )