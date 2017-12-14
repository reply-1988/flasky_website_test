from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from . import main
from .. import db
from .forms import NameForm
from ..modles import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        # 两次输入数据的提醒
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("你似乎改变了你的名字啊=。=")
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False),
                           current_time=datetime.utcnow())