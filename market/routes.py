'''App routes'''
from flask import render_template, redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from market import app, db, bcrypt
from market.model import Item, User
from market.forms import Form, LoginForm, PurchaseForm, SellingForm, ProductDetailsForm



@app.route("/")
@app.route("/home")
def hello():
    "hello world"
    return render_template("home.html")


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market():
    "Market page"
    # items: list[dict] = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 500},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Mobile', 'barcode': '231985128446', 'price': 150}
    # ]

    if request.method == 'POST':
        
        product_id = request.form.get(key='purchased_item', default=None)
        sold_item_id = request.form.get(key='item_sold', default=None)
        product = Item.query.get(product_id) if product_id else None
        item_sold = Item.query.get(sold_item_id) if sold_item_id else None

        if product and current_user.budget >= product.price:
            product.owner = current_user.id
            current_user.budget -= product.price
            db.session.commit()
            flash(f'Congratulations 💐 you have purchased {product.name}', category='info')
        elif item_sold and item_sold.owner == current_user.id:
            item_sold.owner = None
            current_user.budget += item_sold.price
            db.session.commit() 
            flash(f'Congratulations 💐 you have sold {item_sold.name}', category='info')
        else:
            flash(
                f"Sorry 😢 you can\'t purchase {product.name if product else item_sold.name} 💰 Add more money to your budget",
                category='info'
            )
        return redirect('/market')
    
    # GET 
    selling_form = SellingForm()
    purchase_form = PurchaseForm()
    product_details_form = ProductDetailsForm()
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template(
        "market.html",
        items=items,
        owned_items=owned_items,
        purchase_form=purchase_form,
        selling_form=selling_form,
        product_details_form=product_details_form
    )


@app.route('/product_info_update', methods=['POST'])
def product_info():
    '''update product details'''
    item_id = request.form.get(key='item_sold', default=None)
    item = Item.query.get(item_id) if item_id else None
    if item:
        item.name = request.form.get(key='product_info_name')
        item.price = request.form.get(key='product_info_price')
        item.barcode = request.form.get(key='product_info_barcode')
        item.description = request.form.get(key='product_info_description')
        db.session.commit()
    flash(message=f"✅ Product {item.name} updated", category='info')
    return redirect('/market')


@app.route('/create_product', methods=['POST'])
def product_creation():
    '''create new products'''
    product_details = ProductDetailsForm()
    if product_details.validate_on_submit():
        product = Item(
            name=product_details.name.data,
            price=product_details.price.data,
            barcode=product_details.barcode.data,
            description=product_details.description.data,
            owner=current_user.id
        )
        db.session.add(product)
        db.session.commit()
    flash(message=f"✅ Product {product_details.name.data} created", category='info')
    return redirect('/market')


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
            .generate_password_hash(form.password.data.encode('utf-8'))
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
                FORM VALIDATION ERROR 📢 please check the {k} 🔎 {v}
                """,
                category='danger'
            )
        # we can use get_flashed_messages inside HTML templates 
        # just like we use URL_FOR

    return render_template('register.html', form=form)


@app.route(rule='/login', methods=['GET', 'POST'])
def login_page():
    '''Login page'''
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # find the user
        user_in = User.query.filter_by(email=login_form.email.data).first()
        # check if there is a user or not, also check for password match
        if user_in and (
            bcrypt.check_password_hash(
                pw_hash=user_in.password,
                password=login_form.password.data.encode('utf-8')
            )
        ):
            # Greet the user
            flash(
                message=f"Login success 🎉 Welcome {user_in.username}",
                category='success'
            )
            login_user(user_in)
            return redirect('/market')
        else:
            # Error msg
            flash(
                message="Login failed 🤨 Check your email and password",
                category='danger'
            )

    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout_fn():
    '''
    Logs a user out. (You do not need to pass the actual user.) 
    This will also clean up the remember me cookie if it exists.
    '''
    logout_user()
    flash(message="📢 You have been successfully logged out", category='info')
    return redirect('/login')
