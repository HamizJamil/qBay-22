from flask import render_template, request, session, redirect, flash
from qbay.models import *
from qbay import app


def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner

# GET is used to request data from a specified resource.
# POST is used to send data to a server to create/update a resource.
# PUT is used to send data to a server to create/update a resource.


@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        user=request.form["user_email"]
        session["user"] = user
        return render_template("home.html")
    else:
        return render_template("home.html")


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html', message='Please login')


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = login(email, password)
    if user is None: 
        return render_template('login.html', 
                               message='Invalid login credentials')
    else:
        session['user_email'] = email 
        # user is successfully logged in, return to home page
        return redirect('/', code=303)


@app.route('/update-user', methods=['GET'])
def update_user():
    return render_template('update-user.html', 
                           message="Update Profile Information")


@app.route('/update-user', methods=['POST'])
def update_user_post():
    user_email = request.form.get('user_email')
    new_username = request.form.get('username')
    shipping_address = request.form.get('shipping_address')
    postal_code = request.form.get('postal_code')
    if 'user_email' in session:
        new_user = update_user(user_email, new_username, 
                               shipping_address, postal_code)
        if new_user is None:
            return render_template('update-user.html', 
                                   message="New information invalid")
        else:
            return render_template('login.html', 
                                   message="Successfully updated profile!")
    else: 
        return redirect('/login')


@app.route('/logout')
def logout():
    if 'user_email' in session:
        session.pop('user_email', None)
    return redirect('/login')


@app.route('/create-product', methods=['GET']) 
def product_creation(): 
    return render_template('product.html', message="Create Product")


@app.route('/create-product', methods=['POST'])  # sends info to database
def product_creation_post(): 
    product_title = request.form.get('product_title')
    product_description = request.form.get('product_description')
    owner_email = request.form.get('owner_email')
    price = request.form.get('product_price')
    return_message = None

    if product_title.startswith(' '):
        return_message = "ERROR: No Prefixes Allowed in Title"
    if product_title.endswith(' '):
        return_message = "ERROR: No Suffixes Allowed in Title"
    if not product_title.isalnum():
        if " " not in product_title:
            return_message = "ERROR: Title MUST be Alphanumeric"
    product_exists = Product.query.filter_by(product_title=product_title
                                             ).all()
    if int(len(product_exists)) > 0:
        return_message = "ERROR: Product Must Be Unique"
    if int(len(product_description)) < int(len(product_title)):
        return_message = "ERROR: Description Must Be Larger Than Title"
    if int(len(product_description)) < 20:
        return_message = ("ERROR: Description Must Be Larger Than 20" + 
                          "Characters")
    if int(price) > 10000:
        return_message = "ERROR: Price must be Less than $10000 CAD"
    if int(price) < 10:
        return_message = "ERROR: Price must be More than $10 CAD"
    user_exists = User.query.filter_by(user_email=owner_email).first()
    if user_exists == 0:
        return_message = "ERROR: Must Have A Registered Account With QBAY"
    if return_message is None:
        new_product = create_product(product_title, product_description, 
                                     owner_email, price)
        return render_template('product.html', message="Product Created")
    else:
        return render_template('product.html', message=return_message)

    
