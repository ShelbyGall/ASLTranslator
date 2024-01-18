import os

from flask import Flask
from flask_mail import Mail

'''EMAIL INFORMATION START'''
mailSender = None
JWT_SECRET_KEY='F6f`lVCv`:"~6Ze,e|:Njvl:Z`11(fJtytmx7.1R),$fYctn]6z:(amFx)|dn#@'
defaultSenderEmail = "DEFAULT_SENDER_EMAIL"
defaultSenderAppPassword = "DEFAULT_SENDER_APP_PASSWORD"
'''EMAIL INFORMATION END'''

oneTimeSplash = False

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    '''EMAIL INFORMATION START'''
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = defaultSenderEmail
    app.config['MAIL_PASSWORD'] = defaultSenderAppPassword
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['TESTING'] = False
    global mailSender
    mailSender = Mail(app)
    '''EMAIL INFORMATION END'''

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
    #@app.before_first_request
    #splash.splash()
    app.register_blueprint(splash.bp)

    
    #@app.route('/splash')
    #def splash():
    #    return render_template('splash.html')

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    import webbrowser
    global oneTimeSplash
    if oneTimeSplash == False:
        webbrowser.open('http://127.0.0.1:5000/splash')
        oneTimeSplash = True

    return app