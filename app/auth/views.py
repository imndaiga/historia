from flask import url_for, flash, render_template, redirect, request
from ..models import Node
from ..email import send_email
from .forms import EmailRememberMeForm, ChangeEmailForm
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db

@auth.route('/', methods=['GET','POST'])
def request_login():
	form = EmailRememberMeForm()
	if form.validate_on_submit():
		user = Node.query.filter_by(email=form.email.data).first()
		next_url = request.args.get('next')
		if user is not None:
			token = user.generate_login_token(remember_me=form.remember_me.data,
					next_url=next_url, email=form.email.data)
			send_email(user.email, 'MIMINANI Login', 'auth/email/request_login',
				token=token)
			flash('We\'ve sent you a magic login link by email.')
			return redirect(url_for('auth.request_login'))
		n = Node(email=form.email.data)
		db.session.add(n)
		db.session.commit()
		token = n.generate_login_token(remember_me=form.remember_me.data,
				next_url=next_url, email=form.email.data)
		send_email(form.email.data, 'MIMINANI Instructions', 'auth/email/join',
			token=token)
		flash('Thanks for joining us! We\'ve sent you further instructions by email.')
	return render_template('auth/request_login.html', form=form)