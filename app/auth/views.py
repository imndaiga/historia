from flask import url_for, flash, render_template, redirect, request
from ..models import Node
from ..email import send_email
from .forms import EmailRememberMeForm, ChangeEmailForm
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db

@auth.route('/', methods=['GET','POST'])
def welcome():
	form = EmailRememberMeForm()
	if form.validate_on_submit():
		user = Node.query.filter_by(email=form.email.data).first()
		next_url = request.args.get('next')
		if user is not None:
			token = user.generate_login_token(remember_me=form.remember_me.data,
					next_url=next_url, email=form.email.data)
			send_email(user.email, 'Login', 'auth/email/login',
				token=token)
			flash('We\'ve sent you a magic login link by email.')
			return redirect(url_for('auth.welcome'))
		n = Node(email=form.email.data)
		db.session.add(n)
		db.session.commit()
		token = n.generate_login_token(remember_me=form.remember_me.data,
					next_url=next_url, email=form.email.data)
		send_email(form.email.data, 'Instructions', 'auth/email/register',
			token=token)
		flash('Thanks for joining us! We\'ve sent you further instructions by email.')
	return render_template('auth/welcome.html', form=form)

@auth.route('/login/<token>')
def login(token):
	sig_data = Node.node_from_token(token)
	if sig_data['sig']:
		if sig_data['node']:
			if sig_data['node'].confirm_login(token):
				login_data = sig_data['node'].confirm_login(token)
				login_user(sig_data['node'], login_data['remember_me'])
				# return redirect(login_data['next_url'] or url_for('main.index'))
				flash('You are now logged in!')
				return redirect(login_data['next_url'] or url_for('auth.welcome'))
			flash('The magic login link is invalid or has expired.')
			return redirect(url_for('auth.welcome'))
		# Alert admin of possibly malformed tokens
		flash('Eek! Invalid user found. Please register again.')
		return redirect(url_for('auth.welcome'))
	flash('The magic login link is invalid or has expired.')
	return redirect(url_for('auth.welcome'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('auth.welcome'))