from flask_app import app
from flask import request, render_template, session, redirect, flash
from flask_app.models.rent import Rent

#add a new house for rent
@app.route('/rents/new')
def new_house_for_rent():
    if 'user_id' in session:
        return render_template('new_house_for_rent.html')
    return redirect('/')

#CREATE ROUTE
@app.route('/rents/create', methods=['POST'])
def create():
    if (Rent.validate(request.form)):
        data={
            **request.form, 'user_id':session['user_id']
        }
        Rent.add_rent_house(data)
        return redirect('/dashboard') #si les coordonnées données sont correctes, le serveur va amener l'utilisateur à la dashboard si nn;
    return redirect('/rents/new')

#EDIT/UPDATE ROUTES
#EDIT
@app.route('/rents/<id>/edit')
def edit_houses(id):
    if 'user_id' in session:
        r=Rent.get_houses_by_id({'id':id})
        return render_template('edit_houses.html', r=r)

#UPDATE
@app.route('/rents/<id>/update', methods=['POST'])  #method post/action route
def update(id):
    if (Rent.validate(request.form)):
        data={
            **request.form, 'id':int(id)
        }
        r=Rent.edit(data)
        return redirect('/dashboard') 
    return redirect('/rents/'+id+'/edit')

#DELETE
@app.route('/rents/<id>/destroy')
def delete(id):
    if 'user_id' in session: 
        Rent.delete({'id':id})
        return redirect('/dashboard')
    return redirect('/')










































































































