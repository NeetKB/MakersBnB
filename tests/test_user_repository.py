from lib.user import User
from lib.user_repository import *
import pytest

"""test creation of a new user record. username must be unique"""

def test_create_unique_username(db_connection):
    db_connection.seed("seeds/air_makersbnb_test.sql")
    repository = UserRepository(db_connection)
    # repository.create_user(User(None, "Alex", "alexemail@email.com", "password1"))
    with pytest.raises(Exception) as err:
        repository.create_user(User(None, "Alex", "alexemail@email.com", "password1"))
    error_msg = str(err.value)
    assert error_msg == "This username has been taken!"

""" 
create a successful user with details
"""

def test_create_user_success(db_connection):
    db_connection.seed("seeds/air_makersbnb_test.sql")
    repository = UserRepository(db_connection)
    repository.create_user(User(None, "Liam", "liamemail@email.com", "passwo34@5"))
    assert repository.get_user_details("Liam") == User(7, "Liam", "liamemail@email.com", "passwo34@5")

"""
test password does not met special character requirement, raises an error
"""
def test_create_password_special_character_fail(db_connection):
    db_connection.seed("seeds/air_makersbnb_test.sql")
    repository = UserRepository(db_connection)
    with pytest.raises(Exception) as err:
        repository.create_user(User(None, "Jack", "jackemail@email.com", "password1"))
    error_msg = str(err.value)
    assert error_msg == "This passsword does not comply with requirements! Must have atleast one special character"

"""
test password does not length of character requirement, raises an error
"""
def test_create_password_character__length_fail(db_connection):
    db_connection.seed("seeds/air_makersbnb_test.sql")
    repository = UserRepository(db_connection)
    with pytest.raises(Exception) as err:
        repository.create_user(User(None, "Jack", "jackemail@email.com", "passw"))
    error_msg = str(err.value)
    assert error_msg == "This passsword does not comply with requirements! Must have atleast 8 characters"

    # try:
    #     repository.create_user(User(None, "Alex", "dunno@gmail.com", "badpassword"))
    # except Exception as excinfo:
    #     pytest.fail(f"Unexpected exception raised: {excinfo}")

"""test when we call user repository we can read their details"""
def test_read_user_details(db_connection):
    db_connection.seed("seeds/air_makersbnb_test.sql")
    repository = UserRepository(db_connection)
    user = repository.get_user_details("Alex")
    assert user == User(3, "Alex", "alex@example.com", "password£7£89")


""" 

"""
