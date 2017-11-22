from flask import *
from flask_sqlalchemy import SQLAlchemy
from models import *


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
        print("ath_ID = "+str(ath_ID))
        row = Athlete.query.filter_by(ath_ID = ath_ID)
        return render_template('athletebio.html', row = row)


#@app.route('/athletebio', methods = ["GET"])
#def athletebio():
#    print ("ath_ID now = " + str(ath_ID))
#    row = Athlete.query.filter_by(ath_ID = ath_ID)
#    return render_template('athletebio.html', row = row)
