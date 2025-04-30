from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import Ticket
from flask_login import login_required, current_user

user = Blueprint('user', __name__)

@user.route('/submit_ticket', methods=['GET', 'POST'])
@login_required
def submit_ticket():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        ticket = Ticket(title=title, message=message, author=current_user)
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket submitted successfully.', 'success')
        return redirect(url_for('user.submit_ticket'))
    return render_template('submit_ticket.html')
