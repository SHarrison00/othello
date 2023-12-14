# The main.py file is the entry point of our website, and it is the file we 
# execute when we want to start our website. It contains the necessary code to 
# initialize and configure the web application, set up routes, and start the 
# web server to handle incoming requests from users.

from website import create_app

app = create_app()

if __name__ == '__main__': 
    app.run(debug=True) # Production is Falseto