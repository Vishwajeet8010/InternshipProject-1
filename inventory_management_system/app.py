from flask import Flask, render_template, request, redirect, url_for
from models import db, Item, User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Registration Route

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            hashed_password = generate_password_hash(password)  # No need to specify the method
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")  # Print the error to the console for debugging
            return 'An error occurred while registering. Please try again.'
    
    return render_template('register.html')
# User Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the user from the database
        user = User.query.filter_by(username=username).first()
        
        # Verify the password
        if user and check_password_hash(user.password, password):
            return redirect(url_for('dashboard'))  # Redirect to dashboard after successful login
        else:
            return 'Invalid credentials'
    
    return render_template('login.html')

# Dashboard Route (View Items)
@app.route('/dashboard')
def dashboard():
    items = Item.query.all()  # Fetch all items from the database
    return render_template('items.html', items=items)

# Add Item Route
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        
        new_item = Item(name=name, description=description, quantity=quantity)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html')

# Update Item Route
@app.route('/update_item/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.quantity = request.form['quantity']
        
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('update_item.html', item=item)

# Delete Item Route
@app.route('/delete_item/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    return redirect(url_for('dashboard'))

# Run the Flask app
if name == 'main':
    app.run(debug=True)