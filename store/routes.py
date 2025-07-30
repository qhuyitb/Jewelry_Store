import datetime
import os
from flask import flash, redirect, render_template, request, url_for
from flask_mail import Message
import jwt
import stripe
from store import app, db, mail
from store.forms import ChangePassword, ForgotPassword, InfoForm, LoginForm, RegisterForm, ResetPassword
from store.models import Products, Users
from flask_login import current_user, login_required, login_user, logout_user

# home
@app.route('/')
@app.route('/home')
@app.route('/Home')
def home_page():
    products_special = Products.query.filter_by(product_type = 'Special').all()
    return render_template('home_page.html', products_special = products_special)

# about
@app.route('/about')
@app.route('/About')
def about_page():
    return render_template('about_page.html')

# product
@app.route('/product')
@app.route('/Product')
@app.route('/product/category/<string:category>')
def product_page(category=None):
    categories = Products.query.with_entities(Products.category).distinct()
    if category is None or category.lower()=='all':
        products = Products.query.all()
    else:
        products = Products.query.filter_by(category=category).all()
    
   
    return render_template('product_page.html', products = products, categories=categories, selected_category = category)


    
#register
@app.route('/register', methods = ['POST', 'GET'])
@app.route('/Register', methods = ['POST', 'GET'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Create user ....")
        new_user = Users(name=form.username.data,
                         email= form.email.data,
                         )
        new_user.password = form.password1.data
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home_page'))
    else:
        print("create user Error...")
        print(form.errors)
    
    if form.errors != {}:
        for err_mgs in form.errors.values():
            for err in err_mgs:
                flash(f"Error: {err}")
    
    return render_template('register_page.html', form =form)
    
#login
@app.route('/login', methods = ['POST', 'GET'])
@app.route('/Login', methods = ['POST', 'GET']) 
def login_page():
    form  = LoginForm()
    if form.validate_on_submit():
        attempted_user = Users.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
            login_user(attempted_user)
            return redirect(url_for('home_page'))
        else: 
            flash("email or password incorrect", 'danger')

    return render_template('login_page.html', form = form)

#logout    
@app.route('/logout')
@app.route('/Logout')
def logout_page():
    logout_user()
    #flash("You are logout!")
    return redirect(url_for('home_page'))

# Account info
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account_page():
    info_form = InfoForm(prefix='info', obj=current_user)
    pw_form = ChangePassword(prefix='pw')

    if request.method == 'POST':
       
        if info_form.submit.data and info_form.validate():
            info_form.populate_obj(current_user)
            db.session.commit()
            flash('Cập nhật thông tin tài khoản thành công!', 'success')
            return redirect(url_for('account_page'))

        
        if pw_form.submit.data and pw_form.validate():
            if not current_user.check_password(pw_form.old_password.data):
                flash('Mật khẩu cũ không đúng', 'danger')
            else:
                current_user.password = pw_form.new_password.data  
                db.session.commit()
                flash("Đổi mật khẩu thành công", 'success')
            return redirect(url_for('account_page'))

    print('info_form errors:', info_form.errors)
    print('pw_form errors:', pw_form.errors)
    return render_template('account_page.html', info_form=info_form, pw_form=pw_form)

@app.route('/create-checkout-session', methods =['POST'])
def create_checkout_session():
    product_id = request.form.get('product_id')
    product = Products.query.get(product_id)
   
    
    if not product:
        flash("Product not found!", "danger")
        return redirect(url_for('product_page'))

    try:
        # !!!!! tru tam
        product.quantity -= request.form.get('quantity', 1)
        db.session.commit()
       
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(product.price) * 100),  # cents
                    'product_data': {
                        'name': product.name,
                        'description': product.description,
                        'images': [product.image_url] if product.image_url else [],
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success_page', _external=True),
            cancel_url=url_for('cancel_page', _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        print(e)
        flash("Đã xảy ra lỗi khi tạo session thanh toán.", "danger")
        return redirect(url_for('product_page'))
    
    
@app.route('/success')
def success_page():
    
    return 'Thanh toán thành công! Cảm ơn bạn.'

@app.route('/cancel')
def cancel_page():
    return 'Thanh toán bị huỷ.' 



@app.route('/forgot-password', methods =['POST', 'GET'])
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        email = form.email.data
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('Email không tồn tại', 'danger')
            print(('Email không tồn tại'))
            return redirect('/forgot-password')
        token = jwt.encode({
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, os.getenv('JWT_SECRET'), algorithm='HS256')
        
        reset_url = url_for('reset_password', token = token, _external=True)
        msg = Message(subject = 'Đặt lại mật khẩu', recipients=[email])
        msg.body = f"Nhấn vào link để đặt lại mật khẩu: {reset_url}"
        mail.send(msg)
        flash('Đã gửi email đặt lại mật khẩu!', 'success')
        print('Đã gửi email đặt lại mật khẩu!', 'success')
    return render_template('forgot_password.html', form=form)
    
@app.route('/reset-password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    form = ResetPassword()
    try:
        data = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms='HS256')
        email = data['email']
    except jwt.ExpiredSignatureError:
        return 'Token hết hạn'
    except jwt.InvalidTokenError:
        return 'Token không hợp lệ '
    if form.validate_on_submit():
        user = Users.query.filter_by(email=email).first()
        user.password = form.new_password.data
        if user:
            db.session.commit()
            flash('Cập nhật mật khẩu thành công', 'succes')
            return redirect(url_for('login_page'))

    return render_template('reset_password.html', form = form)