import os
from flask import Flask, request, render_template
from lib import space
from lib.database_connection import get_flask_database_connection
from lib.space_repository import SpaceRepository

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /index
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/index
@app.route('/index', methods=['GET'])
def get_index():
    return render_template('index.html')



"""
    SPACES MAIN PAGE
"""
@app.route('/spaces')
def get_spaces():

    connection = get_flask_database_connection(app)
    repository = SpaceRepository(connection)
    list_of_spaces = repository.all()

    return render_template('spaces.html', spaces=list_of_spaces)















# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))


