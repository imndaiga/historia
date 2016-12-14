from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length
from wtforms import ValidationError
from ..models import Person


class EmailRememberMeForm(FlaskForm):
    email = StringField('Email', validators=[
                        Required(), Length(1, 64), Email()])
    remember_me = BooleanField('Keep me logged in')
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[
                        Required(), Length(1, 64), Email()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if Person.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
