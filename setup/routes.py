from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import helpers
from models import SettingsModel, UserModel, db

setup = Blueprint('setup', __name__, template_folder='templates', url_prefix='/setup')


class SetupForm(FlaskForm):
    # website configuration
    website_name = StringField('Website Name', validators=[DataRequired()])

    # initial admin user
    admin_email = StringField('Email', validators=[DataRequired()])
    admin_username = StringField('Username', validators=[DataRequired()])
    admin_password = StringField('Password', validators=[DataRequired()], render_kw={'type': 'password'})
    submit = SubmitField('Finish')


@setup.route('/', methods=['GET', 'POST'])
def configure():
    if SettingsModel.query.filter_by(key='setup_complete').first():
        return redirect(url_for('website.home'))
    else:
        form = SetupForm()
        if form.validate_on_submit():
            helpers.update_setting("setup_complete", "true")
            helpers.update_setting("website_name", form.website_name.data)

            user = UserModel(email=form.admin_email.data, username=form.admin_username.data)
            user.set_password(form.admin_password.data)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        return render_template('setup.html', form=form)
