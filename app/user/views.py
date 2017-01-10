from flask import render_template
from . import user


@user.route('/dashboard/<user>', methods=['GET'])
def dashboard(user):
    return render_template('user/dashboard.html', user=user)
