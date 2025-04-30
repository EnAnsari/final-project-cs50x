from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Ticket
from app.decorators import admin_required, god_required
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/promote/<int:user_id>')
@god_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'user':
        user.role = 'admin'
        db.session.commit()
        flash('User promoted to admin!', 'success')
    else:
        flash('User is already an admin or god.', 'info')
    return redirect(url_for('admin.manage_users'))

@admin.route('/demote/<int:user_id>')
@god_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        user.role = 'user'
        db.session.commit()
        flash('Admin demoted to user.', 'success')
    else:
        flash('Cannot demote this user.', 'info')
    return redirect(url_for('admin.manage_users'))

@admin.route('/manage_users')
@god_required
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@admin.route('/tickets')
@admin_required
def view_tickets():
    tickets = Ticket.query.all()
    return render_template('view_tickets.html', tickets=tickets)

@admin.route('/respond_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@admin_required
def respond_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if request.method == 'POST':
        ticket.response = request.form.get('response')
        db.session.commit()
        flash('Responded to ticket.', 'success')
        return redirect(url_for('admin.view_tickets'))
    return render_template('respond_ticket.html', ticket=ticket)
