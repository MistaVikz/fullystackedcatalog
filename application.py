from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

app = Flask(__name__)

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Routes that return JSON Serialized Data
@app.route('/catalog/JSON')
@app.route('/JSON')
def allCatsJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

@app.route('/catalog/<int:category_id>/items/JSON')
@app.route('/catalog/<int:category_id>/JSON')
def oneCatJSON(category_id):
    category = session.query(Category).filter_by(category_id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])

@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def oneItemJSON(category_id, item_id):
    Catalog_Item = session.query(CatalogItem).filter_by(item_id=item_id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)

# Routes for the CAT-A-LOG Website
@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    return render_template('catalog.html', categories=categories)

@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items')
def catView(category_id):
    category = session.query(Category).filter_by(category_id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catView.html', items=items, category=category)
   
@app.route('/catalog/<int:category_id>/items/new',
            methods = ['GET','POST'])
def itemNew(category_id):
    if request.method == 'POST':
        newItem = CatalogItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template('itemNew.html', category_id=category_id)

    return render_template('itemNew.html', category=category)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def itemEdit(category_id, item_id):
    editItem = session.query(CatalogItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        session.add(editItem)
        session.commit()
        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template(
            'itemEdit.html', category_id=category_id, item_id=item_id, item=editItem)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
            methods=['GET','POST'])
def itemDelete(category_id, item_id):
    deleteItem = session.query(CatalogItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template('itemDelete.html', category_id=category_id, item=deleteItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
