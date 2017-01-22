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
        addRelationForm = AddPersonForm()
        if addRelationForm.validate_on_submit():
            person_exists = Person.query.filter(and_(
                baptism_name=addRelationForm.baptism_name.data,
                ethnic_name=addRelationForm.ethnic_name.data,
                surname=addRelationForm.surname.data,
                sex=addRelationForm.sex.data,
                dob=addRelationForm.date_of_birth.data,
                email=addRelationForm.email.data)).first()
            if person_exists:
                flash('Success!')
            else:
                flash('Person Already Exists')
        return render_template('user/dashboard.html',
                               user=user,
                               addRelationForm=addRelationForm,
                               panel_name='Relationships')
    flash('Please sign in to access profile.')
    return render_template('auth/welcome.html', form=EmailRememberMeForm())
