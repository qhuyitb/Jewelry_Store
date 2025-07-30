from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import Email, EqualTo, ValidationError, DataRequired, Length, Optional, NumberRange
from store.models import Users


class RegisterForm(FlaskForm):
    
    username = StringField(label='User name: ', validators=[Length(2,60), DataRequired()])
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password: ', validators=[Length(6,60), DataRequired()])
    password2 = PasswordField(label='Confirm password: ', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
   
   #check username
    def validate_username(self, field):
        user = Users.query.filter_by(name = field.data).first()
        if user:
            raise ValidationError('User name already exists!, Please choose different user name ')
    
    #check email
    def validate_email(self, field):
        user = Users.query.filter_by(email = field.data).first()
        if user:
            raise ValidationError('Email already exists!, Please choose different email ')

class LoginForm(FlaskForm):
    email = StringField(label='Email: ', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password: ', validators= [DataRequired()])
    submit = SubmitField(label='Sign in')

class InfoForm(FlaskForm):
    name = StringField(label='User name', validators=[DataRequired(), Length(2,60)])
    age = IntegerField(label='Age', validators=[Optional(), NumberRange(1,100)])
    gender = SelectField(label='Gender', choices=[('None', 'None'),('Male', 'Male'), ('Female', 'Female')], validators=[Optional(), Length(2,10)])
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    address = StringField(label='Address', validators=[Optional(), Length(max=255)])
    submit = SubmitField(label='Save Profile')
    
    #check username
    def validate_name(self, field):
        if field.data != current_user.name:
            user = Users.query.filter_by(name = field.data).first()
            if user:
                
                raise ValidationError('User name already exists!, Please choose different user name ')
              
                
    #check email
    def validate_email(self, field):
        if field.data != current_user.email:
            user = Users.query.filter_by(email = field.data).first()
            if user:
                raise ValidationError('Email already exists!, Please choose different Email ')
    
    
class ChangePassword(FlaskForm):
    old_password = PasswordField(label='Password', validators=[DataRequired()])
    new_password = PasswordField(label='Password', validators=[DataRequired(), Length(6,60)])
    confirm_password = PasswordField(label='Password', validators=[DataRequired(), Length(6,60), EqualTo('new_password')])
    submit = SubmitField(label='Save Password')

class ForgotPassword(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email() ])
    submit = SubmitField(label='Gửi link đặt lại mật khẩu')

class ResetPassword(FlaskForm):
    new_password = PasswordField(label='Password', validators=[DataRequired(),Length(6,60) ])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField(label='submit')