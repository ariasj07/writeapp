def decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()  
        print("Something is happening after the function is called.")
    return wrapper

from crud.views import registers
from crud.views import database
database.fetch_database() 