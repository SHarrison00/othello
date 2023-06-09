# In Heroku, the __init__.py file within a folder serves as an entry point for 
# the package. When the folder is imported, the code within the __init__.py 
# file will run automatically. This behavior effectively turns the folder into 
# a package.

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Othello"

    from .views import views
    
    app.register_blueprint(views, url_prefix = "/")

    return app