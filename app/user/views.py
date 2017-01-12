from flask import render_template, flash
from .forms import AddPersonForm
from ..models import Person
from sqlalchemy import and_
from . import user


@user.route('/dashboard/<user>', methods=['GET', 'POST'])
def dashboard(user):
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
    return render_template('user/dashboard.html', user=user, form=form)
