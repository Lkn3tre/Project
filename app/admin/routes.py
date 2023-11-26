from flask import Blueprint, render_template, url_for, flash,request
from werkzeug.utils import redirect
from ..funcs import admin_only
from data.data import *


admin = Blueprint("admin", __name__, url_prefix="/admin", static_folder="static", template_folder="templates")

@admin.route('/items')
@admin_only
def items():
    items = get_all_items()
    return render_template("admin/items.html", items=items)

@admin.route('/')
@admin_only
def dashboard():
    return redirect(url_for('admin.items'))

@admin.route('/add', methods=['POST', 'GET'])
@admin_only
def add():
    if request.method  == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        category = request.form.get('category')
        details = request.form.get('details')
        img_file = request.files['image']
        img_filename = img_file.filename
        img_file.save('app/static/uploads/' + img_filename)
        image = url_for('static', filename=f'uploads/{img_filename}')
        price_id = request.form.get('price_id')
        insert_item(name , price , category , image , details , price_id)
        flash(f'{name} added successfully!','success')
        return redirect(url_for('admin.items'))
    return render_template("admin/add.html",item={})

@admin.route('/edit/<int:id>', methods=['POST', 'GET'])
@admin_only
def edit(id):
    item = get_item_by_id(id)
    if request.method  == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            category = request.form.get('category')
            details = request.form.get('details')
            price_id = request.form.get('price_id')
            img_file = request.files['image']
            img_filename = img_file.filename
            img_file.save('app/static/uploads/' + img_filename)
            image = url_for('static', filename=f'uploads/{img_filename}')
            update_item_by_id(id,name,price,category,image ,details,price_id)
            return redirect(url_for('admin.items'))
    return render_template("admin/add.html",item=item , edit=True)

@admin.route('/delete/<int:id>')
@admin_only
def delete(id):
    item = get_item_by_id(id)
    delete_item_by_id(id)
    flash(f'{item[1]} deleted successfully', 'error')
    return redirect(url_for('admin.items'))