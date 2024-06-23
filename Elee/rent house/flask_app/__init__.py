# __init__.py
from flask import Flask
app = Flask(__name__)


app.secret_key = "shhhhhh"  #it will be used in the session
DATABASE = "python_project"