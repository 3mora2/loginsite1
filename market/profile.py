from flask import render_template
from flask_login import login_required, current_user

from . import app
from .model import LoginDate


@app.route('/profile')
@login_required
def profile_page():
    all_date = LoginDate.query.filter_by(username_id=current_user.id).all()
    all_date = [date.date for date in all_date]
    return render_template('profile.html', all_date=all_date)
