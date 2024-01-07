import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    #------------------------------

    from . import db
    db.init_app(app)
    
    from . import splash
    app.register_blueprint(splash.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

'''
import os

from flask import Flask

# This is the application factory function.
# Any configuration, registration, and other setup the application
# needs will happen inside the application factory function. Then,
# the application will be returned.
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)            # Creates the Flask instance.
                                                                        # __name__ is the name of the current Python module.
                                                                        # instance_relative_config=True tells the app that configuration
                                                                        # files are relative to the instance folder. The instance folder
                                                                        # is located outside the flaskr package and can hold local data
                                                                        # that shouldn’t be committed to version control, such as
                                                                        # configuration secrets and the database file.
    app.config.from_mapping(                                        # Sets some default configuration that the app will use.
        SECRET_KEY='dev',                                               # SECRET_KEY is used by Flask and extensions to keep data safe.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),      # DATABASE is the path where the SQLite database file will be saved.
                                                                        # It’s under app.instance_path, which is the path that Flask has chosen
                                                                        # for the instance folder. You’ll learn more about the database in the
                                                                        # next section
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        # Create the instance folder if it doesn't exist.
        os.makedirs(app.instance_path)                              # os.makedirs() ensures that app.instance_path exists. Flask doesn’t create
                                                                    # the instance folder automatically, but it needs to be created because your
                                                                    # project will create the SQLite database file there.
    except OSError:
        # If the instance folder already exists, don't do anything.
        pass

    # a simple page that says hello
    #@app.route('/')
    @app.route('/hello')                                            # @app.route() creates a simple route so you can see the application working
                                                                    # before getting into the rest of the tutorial. It creates a connection
                                                                    # between the URL /hello and a function that returns a response, the string
                                                                    # 'Hello, World!' in this case.
    def hello():
        return 'Hello, World!'
    
    # Reference db.py
    from . import db
    db.init_app(app)

    # Import and register the blueprint from the factory using app.register_blueprint().
    from . import auth
    app.register_blueprint(auth.bp)

    #from . import blog
    #app.register_blueprint(blog.bp)
    #app.add_url_rule('/', endpoint='index')     # app.add_url_rule() associates the endpoint name 'index'
                                                # with the / url so that url_for('index') or
                                                # url_for('blog.index') will both work, generating the
                                                # same / URL either way.
    
    return app

#app = create_app()
'''