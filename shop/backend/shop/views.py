from shop import app, db
from shop .models import Item, User
from shop .func import allowed_file, isForm, randomId, isFormEdit
from shop .config import UPLOAD_FOLDER, URL_BACKAND, URL_IMAGES, DEFOLD_IMG

from flask import render_template, request, redirect, url_for, flash


import os
from werkzeug.utils import secure_filename
import urllib.request
import cloudipsp 


from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_cors import cross_origin


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename = "uploads/" + filename), code = 301)


@app.route('/', methods = ["GET"])
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template("index.html", data = items)


@app.route('/about', methods = ["GET"])
@login_required
def about():
    return render_template("about.html")


@app.route('/profile', methods = ["GET", "POST"])
@login_required
def profile():
    if current_user.isAdmin:
        return redirect(url_for("index"))  

    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']
        login2 = request.form['login2']
        password2 = request.form['password2']
        user = User.query.get(current_user.id)


        if login == current_user.login and check_password_hash(user.password, password):
            try:
                hash_pwd = generate_password_hash(password2)
                user.login = login2
                user.password = hash_pwd

                db.session.commit()
                flash("Всё успешно прошло")
                return redirect(request.url)
            except:
                flash("Произошла ошибка при добавленни")
                return redirect(request.url)  
        else:
            flash("Логин или пароль не правельны !")
            return redirect(request.url)

    else:
        return render_template("Profile.html")


@app.route('/admin/', methods = ['POST', 'GET'])
def admin():
    if request.method == "POST":
        login = request.form.get('login') 
        password = request.form.get('password')
        user = User.query.filter_by(login = login).first()
       
        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for("admin_display"))
        else:
            flash("Не корректно ввели данные")
            return redirect(request.url)
    else:
        return render_template("admin.html")


@app.route('/admin/adminDisplay', methods = ["GET"])
@login_required
def admin_display():
    if current_user.isAdmin == False:
        return redirect(url_for("index"))  

    items = Item.query.order_by(Item.price).all()
    return render_template("adminDisply.html", items = items, url = request.url) 
    

@app.route('/admin/adminDisplay/All_users', methods = ["GET", "POST"])
def All_users():
    if current_user.isAdmin == False:
        return redirect(url_for("index"))  

    if request.method == "POST":
        user_id = request.form.get("user")
        
        try:
            user = User.query.get(user_id)
            db.session.delete(user)
            db.session.commit()
            flash("Всё успешно прошло !")
            return redirect(request.url)
        except:
            flash("При удалинии произошла ошибка")
            return redirect(request.url)

    else:
        users = User.query.filter(User.isAdmin == False).all()
        return render_template("Allusers.html", users = users)
        

@app.route('/admin/adminDisplay/editItem/<int:id>', methods = ["POST", "GET"])
@login_required
def editItem(id):
    if current_user.isAdmin == False:
        return redirect(url_for("index"))  

    item = Item.query.get(id)

    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        file = request.files['file']
        price_type = request.form['price_type']

        if isFormEdit(request) and title and price:
            path_img = os.path.join(UPLOAD_FOLDER, item.image)

            filename = secure_filename(file.filename)
            filename = randomId(filename)

            try:
                item.title = title
                item.price = price 
                item.price_type = price_type
                
                if file:
                    if item.image != "noImage.png":
                        os.remove(path_img)
                    item.image = filename
                    file.save(os.path.join(UPLOAD_FOLDER, filename))


                db.session.commit() 

                return redirect(url_for("admin_display"))
            except:
                flash("Не предвиденная ошибка")
                return redirect(request.url)    
        else:
            flash("Проверти корректно ли все поля введены")
            return redirect(request.url)
    else:
        return render_template("editItem.html", item = item, back = url_for("admin_display"), url_img = UPLOAD_FOLDER)


@app.route('/admin/adminDisplay/delete/<int:id>', methods = ["GET"])
@login_required
def delete_item(id):
    if current_user.isAdmin == False:
        return redirect(url_for("index")) 

    item = Item.query.get(id)

    path = os.path.join(UPLOAD_FOLDER, item.image)

    try:
        db.session.delete(item)
        db.session.commit()
        if item.image != "noImage.png":
            os.remove(path)
        return redirect(url_for("admin_display"))
    except:
        return render_template("Err.html", info = "Не предвиденная ошибка", back = request.url)
    
    return redirect(url_for("admin"))


@app.route('/admin/adminDisplay/create/', methods = ['GET', 'POST'])
@login_required
def create():
    if current_user.isAdmin == False:
        return redirect(url_for("index")) 

    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']
        price_type = request.form['price_type']
        file = request.files['file']

        

        if title and price:
            if isForm(request):
                filename = secure_filename(file.filename)
                filename = randomId(filename)
            else:
                filename = secure_filename("noImage.png")
                print(filename)
            
            item = Item(title = title, price = price, image = filename, price_type = price_type)
        
            try:
                db.session.add(item)
                
                if isForm(request):
                    print(file)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))

            

                db.session.commit()
                return redirect(url_for("admin_display"))
            except:
                return render_template("Err.html", info = "Получилась ошибка", back = request.url)       
        else:
            return render_template("Err.html", info = "Проверти корректно ли все поля введены", back = request.url)  
    else:
        return render_template("create.html", back = f"/admin/adminDisplay")


@app.route("/details/<int:id>")
@login_required
def details_item(id):
    item = Item.query.get(id)
    return render_template("details.html", item = item)

        
@app.route('/buy/<int:id>')
@login_required
def item_buy(id):
    item = Item.query.get(id)
    
    api = cloudipsp.Api(merchant_id = 1396424, secret_key = 'test') # merchant_id = id компании
    checkout = cloudipsp.Checkout(api=api)

    data = {
        "currency": str(item.price_type),
        "amount": str(item.price) + "000"
    }

    url = checkout.url(data).get('checkout_url')

    
    return redirect(url)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@app.route('/login', methods = ["GET", "POST"])
def Login():
    login = request.form.get('login')
    password = request.form.get('password')


    if login and password:
        user = User.query.filter_by(login = login).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)

            return redirect(url_for("index"))
        else:
            flash("Логин или пароль не корректно введены !")
    else:
        flash("Логин или пароль не введенны")

    return render_template("Login.html")


@app.route('/register', methods = ["GET", "POST"])
def Register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')


    if request.method == "POST":
        if not (login or password or password2):
            flash("Вы заполнели не все поля !")
        elif password != password2:
            flash("Не корректно введён пароль") 
        else: 
            try:
                hash_pwd = generate_password_hash(password)
                new_user = User(login = login, password = hash_pwd)

                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("Login"))
            except:
                flash("Ошибка при добавлении пользователя")
                return render_template("Register.html")  
    else:
        return render_template("Register.html") 
    
    return render_template("Register.html") 


@app.route('/logout', methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.after_request
def redirect_signin(response):
    if response.status_code == 401:
        return redirect(url_for('Login') + "?next=" + request.url)
    
    return response


if __name__ == "__main__":
    app.run(debug = True)