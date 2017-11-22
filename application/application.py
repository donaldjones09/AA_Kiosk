from flask import *
from flask_sqlalchemy import SQLAlchemy
from models import *

ath_ID = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/athleteindex', methods = ["GET"])
def athleteindex():
    if request.method == "GET":
        rows = Athlete.query.all()
        return render_template('athleteindex.html', rows = rows)
    else:
        ath_ID = request.form.get['athlete']
        return redirect(url_for('athletebio'))


@app.route('/athletebio', methods = ["GET"])
def athletebio():
    athlete = Athlete.query.filter_by(ath_ID = ath_ID)
    return render_template('athletebio.html')
