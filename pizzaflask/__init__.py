from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flaskpizza import routes

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=5555)
