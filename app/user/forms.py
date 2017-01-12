from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField
from wtforms.validators import Required, Email, Length


class AddPersonForm(FlaskForm):
    sex_choices = [(1, 'Select Any'), (2, 'Male'), (3, 'Female')]
    baptism_name = StringField('Baptism Name', validators=[
        Required(),
        Length(1, 64)])
    ethnic_name = StringField('Ethnic Name', validators=[
        Required(),
        Length(1, 64)])
    surname = StringField('Surname/Family Name', validators=[
        Required(),
        Length(1, 64)])
    sex = SelectField(choices=sex_choices, default=['1'])
    date_of_birth = DateField('Date of Birth')
    email = StringField('Email', validators=[Email(), Length(1, 64)])
    submit = SubmitField('Add')
