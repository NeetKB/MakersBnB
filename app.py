import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import get_flask_database_connection
from lib.booking_repository import BookingRepository
from lib.booking import Booking
from lib.space import Space
from lib.space_repository import SpaceRepository
from lib.user import User
from lib.user_repository import UserRepository
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)
app.secret_key = 'super secret key'

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

#------------------- LOGIN ROUTES -------------------#

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    connection = get_flask_database_connection(app)
    repo = UserRepository(connection)
    username = request.form['username']
    password = request.form['password']

    if repo.check_password(username, password) == True:
        user = repo.get_user_details(username)
        # Set the user ID in session
        session['user_id'] = user.id

        # return render_template('spaces.html')
        return redirect(location="/spaces")
    else:
        errors = "Incorrect username or password"
        return render_template('login.html', errors=errors)

# if title == "" or release_year == "" or artist_id == "":
#         errors = "Title, release year and artist id cannot be blank"
#         return render_template('/albums/new.html', errors=errors)
    
#     album = Album(None, title, release_year, artist_id)
#     repo.create_album(album)
#     return redirect(f"/single_album/{album.id}")

#------------------- SPACES ROUTES -------------------#

@app.route('/spaces')
def get_spaces():

    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    list_of_spaces = repository.all()

    return render_template('spaces.html', spaces=list_of_spaces)


@app.route('/create_space')
def get_create_space():
    return render_template('/create_space.html')


@app.route('/create_space', methods=["POST"])
def create_space():
    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    name = request.form["name"]
    description = request.form["description"]
    price = request.form["price"]
    user_id = request.form["user_id"]

    space = Space(None, name, description, price, user_id)

    try:
        space_id = repository.create(space)
        return render_template("/create_space_success.html", id = space_id)
    
    except Exception as e:
        error = str(e)
        return render_template("/create_space.html", error=error)


@app.route('/create_space_success')
def create_space_successful():
    return render_template('/create_space_success.html)')


@app.route('/spaces/<int:id>')
def view_space(id):

    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)

    space = repository.find(id)
    return render_template("/view_space.html", space=space)

#------------------- REGISTER ROUTES -------------------#

@app.route('/register')
def get_register_page():
    return render_template('/register.html')



@app.route('/register', methods=["POST"])
def register_user():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    user = User(None, username, email, password)

    try:
        repository.create_user(user)
        return render_template("/register_success.html")
    
    except Exception as e:
        error = str(e)
        return render_template("/register.html", error=error)



@app.route('/register_success')
def register_successful():
    return render_template('/register_success.html)')


#------------------- BOOKING ROUTES -------------------#

@app.route('/booking/<int:space_id>', methods=["GET"])
def get_booking_form(space_id):
    return render_template('booking_form.html', user_id = session["user_id"], space_id = space_id)


@app.route('/post_booking/<int:space_id>', methods=["POST"])
def post_booking(space_id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    date = request.form['date_booked']
    date_str = request.form['date_booked']
    date = datetime.strptime(date_str, '%Y-%m-%d').date()    
    booking = Booking(
        None,
        date,
        'pending',
        session["user_id"],
        space_id
        )
    try: 
        booking = repo.create(booking)
        print(repo.is_date_unavailable(booking))
        return redirect(f'/booking_complete/{booking.id}')
    except Exception as e:
        error =  str(e)
        # pass error in html
        print(repo.is_date_unavailable(booking))
        return render_template('booking_form.html', space_id=space_id, error=error)
    
    

@app.route('/booking_complete/<int:id>', methods=['GET'])
def get_booking(id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    booking = repo.get_booking(id)
    return render_template('booking.html', booking = booking)



@app.route('/booking_confirmed/<int:booking_id>', methods=["PUT"])
def put_booking(booking_id):
    connection = get_flask_database_connection(app)
    repo = BookingRepository(connection)
    booking = repo.confirm_booking(booking_id)
    return '' , 200

    
    

# space needs to display available bookings (get) via user id
# user_id to find their spaces -> space_id to find available bookings -> for that space  

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    
    app.config['SESSION_TYPE'] = 'filesystem'

    session.init_app(app)
