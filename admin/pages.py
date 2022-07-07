import random

from flask import url_for, Blueprint, request, flash, render_template
from flask_login import login_required
from werkzeug.utils import redirect

from models import PageModel, db

pages = Blueprint('pages', __name__, template_folder='templates', url_prefix='/pages')


@pages.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if id == "new":
        # create a new page
        # random number to make sure the url is unique
        number = random.randint(1, 10000)
        page = PageModel(name=f'New Page #{number}', url=f'newpage{number}',
                         content='<h1>I am new page</h1>', include_blog=False)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for('admin.pages.edit', id=page.id))
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
            flash('Page successfully updated!', 'success')
            return redirect(url_for('admin.pages'))
    return render_template('admin/edit_page.html', page=page)


@pages.route('/delete/<id>', methods=['GET'])
@login_required
def delete(id):
    page = PageModel.query.filter_by(id=id).first()
    if page is None:
        flash('Page not found!', 'danger')
        return redirect(url_for('admin.pages'))
    db.session.delete(page)
    db.session.commit()
    flash(f'Page \"{page.name}\" successfully deleted!', 'success')
    return redirect(url_for('admin.pages'))
