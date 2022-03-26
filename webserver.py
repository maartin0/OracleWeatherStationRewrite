from flask import Flask

app = Flask(__name__)

from database import Database
from constants import HEADERS

db = Database(HEADERS)

@app.route("/")
def index():
    return db.content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
