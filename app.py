from flask.cli import load_dotenv
from flask import Flask, request, jsonify #importing flask application class, request allows us to read the data sent to the client
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy it bascially translates python operation into SQL
#SQLAlchemy also uses ORM=Object Relational Mapping without ORM we may write the raw sql queries in our application

import os
#from app import app                         
from dotenv import load_dotenv
from routes.job_routes import job_bp  #importing job_bp from job_routes
from extensions import db, jwt
from routes.auth_routes import auth_bp
from flask_migrate import Migrate   #this is used for migration of the database
load_dotenv()

def create_app(test_config=None):

    app = Flask(__name__)

    if test_config is None:

        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobtrack.db"

        app.config["JWT_SECRET_KEY"] = os.getenv(
            "JWT_SECRET_KEY"
        )

    else:

        app.config.update(test_config)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    jwt.init_app(app)

    Migrate(app, db)

    app.register_blueprint(job_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return "Welcome to Job Application!!"

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)


'''app = Flask(__name__) # This creates our Flask application. Jsonify helps us to return the results properly in json


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobtrack.db" #Tells flask to use sqlite database name as jobtrack.db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

#app.config["JWT_SECRET_KEY"] = "supersecretkey"
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
db.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(job_bp) #this is where we register the job_blueprint
app.register_blueprint(auth_bp) #this is where we register the auth_bp


@app.route("/")
def home():
    return "Welcome to Job Application"

if __name__ == "__main__":
    app.run(debug=True)'''

