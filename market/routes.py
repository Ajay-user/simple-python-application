'''App routes'''
from flask import render_template, redirect, flash

from market import app, db, bcrypt
from market.model import Item, User
from market.forms import Form



@app.route("/")
@app.route("/home")
def hello():
    "hello world"
    return render_template("home.html")


@app.route("/market")
def market():
    "Market page"
    # items: list[dict] = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Mobile', 'barcode': '231985128446', 'price': 150}
    # ]
    items = Item.query.all()
    return render_template("market.html", items=items)


# @app.route("/about/<user>")
# def about(user: str = 'user'):
#     "hello user | DYNAMIC ROUTE"
#     return f"hello {user}"


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    '''user registration route'''
    form = Form()

    if form.validate_on_submit():

        password_hash = (
            bcrypt
            .generate_password_hash(form.password.data)
            .decode('utf-8')
        )
        
        user_to_create = User(
            username=form.username.data,
            email=form.email.data,
            password=password_hash)
        
        db.session.add(user_to_create)
        db.session.commit()
        return redirect('/market')
    
    # if there are any form validation errors we've to alert the user
    # form.errors [dict] contains all the validation errors as KEY:VAL pair
    if form.errors:
        # use built-in FLASH function to display info in html template
        for k, v in form.errors.items():
            flash(
                message=f"""
                FORM VALIDATION ERROR | please check the {k} | {v}
                """,
                category='danger'
            )
        # we can use get_flashed_messages inside HTML templates 
        # just like we use URL_FOR

    return render_template('register.html', form=form)



