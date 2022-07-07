from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import current_user, login_user, login_required

import config
from models import UserModel, db, PageModel, NavbarItemModel, SettingsModel

from admin.pages import pages
from admin.navbar_items import navbar_items

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

admin.register_blueprint(pages)
admin.register_blueprint(navbar_items)


@admin.route('/')
@login_required
def home():
    return render_template('admin/home.html')


@admin.route('/pages')
@login_required
def pages():
    return render_template('admin/pages.html', pages=PageModel.query.all())


@admin.route('/navbar_items')
@login_required
def navbar_items():
    return render_template('admin/navbar_items.html', items=NavbarItemModel.query.all())


@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = {}
    for setting in SettingsModel.query.all():
        settings[setting.key] = setting.value
    if request.method == 'POST':
        # update settings in database
        for key in settings:
            if key in request.form:
                setting = SettingsModel.query.filter_by(key=key).first()
                # check if changed
                if setting.value != request.form[key]:
                    setting.value = request.form[key]
                    db.session.commit()
                    flash(f'Successfully updated setting \"{setting.key}\"', 'success')
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', pages=PageModel.query.all(), settings=settings)


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))

    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email=email).first()
        remember = False

        if request.form['remember'] != "No":
            remember = True

        if user is not None and user.check_password(request.form['password']):
            login_user(user, remember=remember)
            return redirect('/')

    return render_template('login.html')


@admin.route('/register', methods=['POST', 'GET'])
def register():
    if config.allow_admin_register:
        if current_user.is_authenticated:
            return redirect('/')

        if request.method == 'POST':
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            if UserModel.query.filter_by(email=email).first():
                return 'Email already in use'
            user = UserModel(email=email, username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect('/admin/login')
        return render_template('register.html')
    else:
        return 'Registration is disabled'
