from flask import Flask, render_template, request, redirect, url_for, session, flash # type: ignore
from data import *  # Import MongoDB setup
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

app = Flask(__name__)
app.secret_key = 'sri'  # For session management

# Route for Signin
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['User']
        password = request.form['pass']
        # Fetch user from the database
        user = Users.objects(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return redirect(url_for('dashboard'))  # Redirect to the dashboard or home page
        else:
            flash("Invalid username or password. Please try again or sign up.", "error")
            return redirect(url_for('signin'))
    return render_template('signin.html')

# Route for Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['User']
        password = generate_password_hash(request.form['pass'])
        email = request.form['email']
        phone = request.form['phone']
        
        # Check if user already exists
        if Users.objects(username=username).first():
            flash("Username already exists. Please choose a different username.", "error")
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = Users(username=username, password=password, email=email, phone=phone)
        new_user.save()
        
        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for('signin'))
    return render_template('signup.html')

# Route for Signout
@app.route('/signout')
def signout():
    session.pop('username', None)
    flash("You have been signed out.", "info")
    return redirect(url_for('signin'))

# Dashboard or main page after login
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash("Please sign in to access the dashboard.", "warning")
        return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(debug=True,port=1234)
