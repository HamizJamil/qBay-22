from qbay.models import *


# using assert keyword to run checks with global backend functions
def test_register_update():
    assert register_user('profiletest', 'update@gmail.com', 'ABC@abc') is True


def test_r1_user_register():
    # checking 3 different user situations where 3rd pw is missing special char
    assert register_user('u0X', 'test0@test.com', 'eA123456!') is True
    assert register_user('u0X', 'test1@test.com', 'eA123456!') is True
    assert register_user('u0X', 'test0@test.com', '123456') is False


def test_r2_login():
    # checking a fake user login and verifying its username credential
    user = login('test0@test.com', 'eA123456!')
    assert user is not None
    assert (user.user_name == 'u0X') is True
    # testing login with wrong credentials
    user = login('test0@test.com', 'eA123456')
    assert user is None


def test_r3_user_update():
    # taking passed users from r1 and and checking that the added addy/postal
    # code is valid by returning a user object
    assert update_user('test0@test.com', 'u1X', '99 University Ave Kingston',
                       'K7L 3N6') is not None
    # testing with incorrect addy sequence resulting in no returned user
    assert update_user('test1@test.com', 'u1X', '9! University Ave Kingston ',
                       'K7L 3N6') is None


def test_r4_product_create():
    # testing creating a product with proper credentials
    assert create_product('iPhone11X New', 'Brand New iPhone11X 2020',
                          'test0@test.com', 12) is True
    assert create_product('Gloves', 'Winning Gloves 12 Oz',
                          'test0@test.com', 15) is True
    # testing creating a product with different correct credentials
    assert create_product('iPhone11X Pro', 'This iPhone is so powerful',
                          'test1@test.com', 20) is True
    assert create_product('Ferrari', 'Cherry Red, 10,000km ONLY!',
                          'test1@test.com', 100) is True
    # testing product failure with too small of description
    assert create_product('iPhone11X', ' New ', 'test0@test.com', 10) is False


def test_r5_product_update():
    # testing updating a prodcut with new description and price
    assert update_product('iPhone11X New', 'test0@test.com', 33,
                          "Coolest Phone Ever", None) is not None
    assert update_product('iPhone11X Pro', 'test1@test.com', 25, None,
                          "256GB storage and fast") is not None
    # incorrectily updating product with price decrease
    assert update_product('iPhone11X New', 45, "Coolest Phone Ever", None
                          ) is None


def test_r6_create_review():
    # creating a review with int score
    assert create_review('test1@test.com', 6, "This phone is so good") is True
    # creating bad review with text score
    assert create_review('test0@test.com', "Six", "This phone is so good"
                         ) is False


def test_r7_display_products_before_purchase():
    current_user = 'test0@test.com'
    assert display_products(current_user) is not None


def test_r8_create_transaction():
    current_user = 'test0@test.com'
    product_bought = Product.query.filter_by(title='iPhone11X Pro'
                                             ).first()
    product_id = product_bought.id
    # successful purchase 
    assert create_transaction(current_user, product_id) is True
    # checking that you cannot buy same product over again
    assert create_transaction(current_user, product_id) is False
    # checking that you cannot buy your own product
    product_bought2 = Product.query.filter_by(title='Gloves'
                                              ).first()
    product_id2 = product_bought2.id                                    
    assert create_transaction(current_user, product_id2) is False
    # checking that you cannot buy product over fund amount
    product_bought3 = Product.query.filter_by(title='Ferrari'
                                              ).first()
    product_id3 = product_bought3.id                                    
    assert create_transaction(current_user, product_id3) is False


def test_r9_display_products():
    current_user = 'test0@test.com'
    assert display_products(current_user) is not None

