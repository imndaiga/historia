from flask import render_template, flash
from .forms import AddPersonForm
from ..auth.forms import EmailRememberMeForm
from ..models import Person
from sqlalchemy import and_
from flask_login import login_required, current_user
from . import user


@user.route('/<user>/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard(user):
    if current_user.baptism_name == user or \
       current_user.email.split('@')[0] == user:
        addPersonForm = AddPersonForm()
        if addPersonForm.validate_on_submit():
            person_exists = Person.query.filter(and_(
                baptism_name=addPersonForm.baptism_name.data,
                ethnic_name=addPersonForm.ethnic_name.data,
                surname=addPersonForm.surname.data,
                sex=addPersonForm.sex.data,
                dob=addPersonForm.date_of_birth.data,
                email=addPersonForm.email.data)).first()
            if person_exists:
                flash('Success!')
            else:
                flash('Person Already Exists')
        return render_template('user/dashboard.html',
                               user=user,
                               addPersonForm=addPersonForm)
    flash('Please sign in to access profile.')
    return render_template('auth/welcome.html', form=EmailRememberMeForm())
