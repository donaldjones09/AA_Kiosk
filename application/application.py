from flask import *
from flask_sqlalchemy import SQLAlchemy
from models import *

app.secret_key = b'\xeev\xc5\xe0\x0c9\x94\x1f\xad\xff\x02\xc2\xaa_bx\x0e\xf3*\x05\x01"\x02:'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/athleteindex', methods = ["GET", "POST"])
def athleteindex():
    if request.method == "GET":
        rows = Athlete.query.all()
        return render_template('athleteindex.html', rows = rows)
    else:
        ath_ID = int(request.form.get("athlete"))
        session['ath_ID'] = ath_ID
        return redirect(url_for('athletebio'))

@app.route('/athletebio', methods = ["GET"])
def athletebio():
    ath_ID = int(session.get("ath_ID"))
    athlete = Athlete.query.filter_by(ath_ID = ath_ID).first()
    return render_template('athletebio.html', row = athlete)
