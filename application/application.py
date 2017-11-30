from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
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
        session['ath_ID'] = ath_ID
        return redirect(url_for('athletebio'))

@app.route('/athletebio', methods = ["GET"])
def athletebio():
    ath_ID = int(session.get("ath_ID"))
    athlete = Athlete.query.filter_by(ath_ID = ath_ID).first()
    return render_template('athletebio.html', row = athlete)

@app.route('/coachindex', methods = ["GET", "POST"])
def coachindex():
    if request.method == "GET":
        rows = Coach.query.all()
        return render_template('coachindex.html', rows = rows)
    else:
        coach_ID = int(request.form.get("coach"))
        session['coach_ID'] = coach_ID
        return redirect(url_for('coachbio'))

@app.route('/coachbio', methods = ["GET"])
def coachbio():
    coach_ID = int(session.get("coach_ID"))
    coach = Coach.query.filter_by(coach_ID = coach_ID).first()
    #raw SQL to query every photo that the selected coach is in
    rows = db.engine.execute("SELECT year, filename, sport_name FROM photo_seating INNER JOIN photos on photo_seating.pic_ID = photos.pic_ID INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE coach_ID = coach_ID")

    return render_template('coachbio.html', coach = coach, rows = rows)
