import random

from flask import Blueprint, request, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required

import config
from models import UserModel, db, PageModel, NavbarItemModel, SettingsModel

admin = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


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
                setting.value = request.form[key]
                db.session.commit()
        return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html', pages=PageModel.query.all(), settings=settings)


@admin.route('/navbar_items/edit/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def edit_navbar_item(id):
    if id == "new":
        # find the last item in the list and use its position_index + 1
        last_item = NavbarItemModel.query.order_by(NavbarItemModel.position_index.desc()).first()
        if last_item:
            position_index = last_item.position_index + 1
        else:
            position_index = 1
        # create a new item
        item = NavbarItemModel(position_index=position_index, title="New Item")
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('admin.edit_navbar_item', id=item.id))
    else:
        item = NavbarItemModel.query.filter_by(id=id).first()
        if item is None:
            return redirect(url_for('admin.navbar_items'))
        if request.method == 'POST':
            item.title = request.form['title']
            item.custom_url = request.form['custom_url']
            if 'custom_url_enabled' in request.form:
                item.custom_url_enabled = request.form['custom_url_enabled'] == 'on'
            else:
                item.custom_url_enabled = False
            item.position_index = request.form['index']
            item.page_id = request.form['page_id']
            db.session.commit()
            return redirect(url_for('admin.navbar_items'))
        if request.method == 'DELETE':
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('admin.navbar_items'))
    return render_template('admin/edit_navbar_item.html', item=item, pages=PageModel.query.all())


@admin.route('/pages/edit/<id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def edit_page(id):
    if id == "new":
        # create a new page
        # random number to make sure the url is unique
        number = random.randint(1, 10000)
        page = PageModel(name=f'New Page #{number}', url=f'newpage{number}',
                         content='<h1>I am new page</h1>', include_blog=False)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('admin.edit_page', id=page.id))
    else:
        page = PageModel.query.filter_by(id=id).first()
        if page is None:
            return redirect(url_for('admin.pages'))
        if request.method == 'POST':
            page.name = request.form['name']
            page.url = request.form['url']
            page.content = request.form['content']
            page.include_blog = request.form['include_blog'] == 'on'
            db.session.commit()
            return redirect(url_for('admin.pages'))
        if request.method == 'DELETE':
            db.session.delete(page)
            db.session.commit()
            return redirect(url_for('admin.pages'))
    return render_template('admin/edit_page.html', page=page)


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
