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
        rows = Athlete.query.order_by(Athlete.Lname).all()
        return render_template('athleteindex.html', rows = rows)
    else:
        ath_ID = int(request.form.get("athlete"))
        session['ath_ID'] = ath_ID
        return redirect(url_for('athletebio'))

@app.route('/athletebio', methods = ["GET"])
def athletebio():
    ath_ID = int(session.get("ath_ID"))
    athlete = Athlete.query.filter_by(ath_ID = ath_ID).first()
    #raw SQL to query every photo that the selected coach is in
    rows = db.engine.execute("SELECT year, filename, sport_name FROM photo_seating INNER JOIN photos on photo_seating.pic_ID = photos.pic_ID INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE ath_ID == :ath_ID", ath_ID = ath_ID)
    return render_template('athletebio.html', athlete = athlete, rows = rows)

@app.route('/coachindex', methods = ["GET", "POST"])
def coachindex():
    if request.method == "GET":
        rows = Coach.query.order_by(Coach.Lname).all()
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
    rows = db.engine.execute("SELECT year, filename, sport_name FROM photo_seating INNER JOIN photos on photo_seating.pic_ID = photos.pic_ID INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE coach_ID == :coach_ID", coach_ID = coach_ID)

    return render_template('coachbio.html', coach = coach, rows = rows)

@app.route('/sportindex', methods = ["GET", "POST"])
def sportindex():
    if request.method == "GET":
        rows = Sport.query.order_by(Sport.sport_name).all()
        return render_template('sportindex.html', rows = rows)
    else:
        sport_ID = int(request.form.get("sport"))
        session['sport_ID'] = sport_ID
        return redirect(url_for('sporthome'))

@app.route('/sporthome', methods = ["GET"])
def sporthome():
    sport_ID = int(session.get("sport_ID"))
    sport = Sport.query.filter_by(sport_ID = sport_ID).first()
    #raw SQL to query every photo of the selected sport
    rows = db.engine.execute("SELECT year, filename FROM photos INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE sports.sport_ID == :sport_ID", sport_ID = sport_ID)
    return render_template('sporthome.html', sport = sport, rows = rows)

@app.route('/yearindex', methods = ["GET", "POST"])
def yearindex():
    if request.method == "GET":
        rows = db.engine.execute("SELECT DISTINCT year FROM photos")
        return render_template('yearindex.html', rows = rows)
    else:
        year = int(request.form.get("year"))
        session['year'] = year
        return redirect(url_for('yearhome'))

@app.route('/yearhome', methods = ["GET"])
def yearhome():
    year = int(session.get("year"))
    pictures = db.engine.execute("SELECT sport_name, filename FROM photos INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE photos.year == :year", year = year)
    return render_template('yearhome.html', year = year, rows = pictures)
