from flask_app import app, ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import render_template ,redirect,request,flash,session
from flask_app.models.house import House
import os
from werkzeug.utils import secure_filename
import uuid

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/buy/house')
def get_houses_for_sale():
    houses=House.select_all_houses_for_sale_with_pic()
    return render_template('all_houses_for_sale.html',houses=houses)


@app.route('/sell/house')
def put_a_house_to_sell():
    return render_template('create_a_house_to_sell.html')

@app.post('/create/house/sell')
def sell_the_house():
    data={
        'user_id':session['user_id'],
        **request.form
    }
    
    new_house_id=House.create_a_house(data)
    return redirect('/house/pics_forhouse/'+str(new_house_id))

@app.post('/house/pics/insert')
def insert_pics_to_the_house_to_sell():
    print("IMAGE FORM-----",request.form)
    print("IMAGE FiLE-----",request.files)
    file = request.files['path']
<<<<<<< HEAD
    data={
        'house_id':int(request.form['house_id']),
        'path':request.files['path'].filename
    }
    House.put_photos_for_the_house(data)
    
    return redirect(f'/house/{request.form['house_id']}')
=======
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Generate a UUID for the filename
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))

        data = {
            **request.form,
            'path': unique_filename
        }
        House.put_photos_for_the_house(data)
    return redirect(f'/house/pics_forhouse/{request.form['house_id']}')
>>>>>>> 299f716b18f62f5b26e9532d7d3a3de8bdb87446

@app.route('/house/pics_forhouse/<int:id>')
def get_house_by_id(id):
    return render_template('on_house.html', data=id)



