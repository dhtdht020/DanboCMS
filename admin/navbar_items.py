import random

from flask import url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from werkzeug.utils import redirect

from models import PageModel, db, NavbarItemModel

navbar_items = Blueprint('navbar_items', __name__, template_folder='templates', url_prefix='/navbar_items')


@navbar_items.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
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
        return redirect(url_for('admin.navbar_items.edit', id=item.id))
    else:
        item = NavbarItemModel.query.filter_by(id=id).first()
        if item is None:
            flash('Item not found!', 'danger')
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
            flash('Item successfully updated!', 'success')
            return redirect(url_for('admin.navbar_items'))
    return render_template('admin/edit_navbar_item.html', item=item, pages=PageModel.query.all())


@navbar_items.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    item = NavbarItemModel.query.filter_by(id=id).first()
    if item is None:
        flash('Item not found!', 'danger')
        return redirect(url_for('admin.navbar_items'))
    db.session.delete(item)
    db.session.commit()
    flash(f'Navigation bar item \"{item.title}\" successfully deleted!', 'success')
    return redirect(url_for('admin.navbar_items'))
