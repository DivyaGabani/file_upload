import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for,current_app
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.db import db
from app.db.models import Transaction
from app.transactions.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

transactions = Blueprint('transactions', __name__,
                        template_folder='templates')

@transactions.route('/transactions', methods=['GET'], defaults={"page": 1})
@transactions.route('/transactions/<int:page>', methods=['GET'])
def transactions_browse(page):
    page = page
    per_page = 1000
    pagination = Transaction.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    start_amt = 0
    if current_user.bal is None:
        start_amt = 0
    else:
        start_amt = current_user.bal
    try:
        return render_template('browse_transactions.html',data=data,pagination=pagination,start_amt=start_amt)
    except TemplateNotFound:
        abort(404)

@transactions.route('/transactions/upload', methods=['POST', 'GET'])
@login_required
def transactions_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        #user = current_user
        if current_user.bal is None:
            amt = current_user.start_balance
        else:
            amt = current_user.bal
        list_of_transactions = []
        with open(filepath, encoding='utf-8-sig') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_transactions.append(Transaction(row['AMOUNT'], row['TYPE']))
                amt = amt + int(row['AMOUNT'])

        current_user.transactions = list_of_transactions
        current_user.set_bal(amt)
        current_user.start_balance = amt
        db.session.commit()
        return redirect(url_for('transactions.transactions_browse'))

    try:
        return render_template('uploadt.html', form=form)
    except TemplateNotFound:
        abort(404)
