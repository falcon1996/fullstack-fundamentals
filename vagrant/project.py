from flask import Flask , render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def DefaultRestaurantMenu():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.ids)
    output = ''
    for i in items:
        output += i.name
	output += '</br>'
	output += i.price
	output += '</br>'
	output += i.description
	output += '</br>'
	output += '</br>'

    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(ids=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.ids)
    return render_template('menu.html',restaurant = restaurant, items = items)   #opens new webpage for post request

    """
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br></br>'
        return output
    """


#Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New menu item ceated!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

#Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    oldItem = session.query(MenuItem).filter_by(ids = menu_id).one()
    if request.method == 'POST':
        newItem = request.form['name']
        oldItem.name = newItem
        session.add(oldItem)
        session.commit()
        flash("Menu item edited!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=oldItem)


#Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemtoDelete = session.query(MenuItem).filter_by(ids=menu_id).one()
    if request.method == 'POST':
        session.delete(itemtoDelete)
        session.commit()
        flash("Menu item deleted!!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))

    else:
        return render_template('deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemtoDelete)

if __name__ == '__main__':
    app.secret_key='super_secret_key'
    app.debug = True  # Server will reload itself eachtime it notices codechange
    app.run(host = '0.0.0.0', port = 5000)
