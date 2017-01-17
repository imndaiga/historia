from flask import render_template, flash
from .forms import AddPersonForm
from ..auth.forms import EmailRememberMeForm
from ..models import Person
from sqlalchemy import and_
from flask_login import login_required, current_user
from . import user


@user.route('/dashboard/<user>', methods=['GET', 'POST'])
@login_required
def dashboard(user):
    if current_user.baptism_name == user or \
       current_user.email.split('@')[0] == user:
        return render_template('user/dashboard.html',
                               user=user,
                               panel_name='Overview')
    flash('Please sign in to access profile.')
    return render_template('auth/welcome.html', form=EmailRememberMeForm())


@user.route('/dashboard/<user>/add_person', methods=['GET', 'POST'])
@login_required
def add_person(user):
    if current_user.baptism_name == user or \
       current_user.email.split('@')[0] == user:
        form = AddPersonForm()
        if form.validate_on_submit():
            person_exists = Person.query.filter(and_(
                baptism_name=form.baptism_name.data,
                ethnic_name=form.ethnic_name.data,
                surname=form.surname.data,
                sex=form.sex.data,
                dob=form.date_of_birth.data,
                email=form.email.data)).first()
            if person_exists:
                flash('Success!')
            else:
                flash('Person Already Exists')
        return render_template('user/add_person.html',
                               user=user,
                               form=form,
                               panel_name='Relationships')
    flash('Please sign in to access profile.')
    return render_template('auth/welcome.html', form=EmailRememberMeForm())
