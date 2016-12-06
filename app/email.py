from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    # print('Sending email to {} with the subject of {} using {}
    # template containing {}'.format(to,subject,template,token))
    app = current_app._get_current_object()
    msg = Message(app.config['MIMINANI_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MIMINANI_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
