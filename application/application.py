from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from models import *
import string

#DONE
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
    #raw SQL to query every photo that the selected athlete is in
    rows = db.engine.execute("SELECT year, filename, sport_name FROM photo_seating INNER JOIN photos on photo_seating.pic_ID = photos.pic_ID INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE ath_ID == :ath_ID", ath_ID = ath_ID)
    return render_template('athletebio.html', athlete = athlete, rows = rows)

#DONE
@app.route('/coachindex', methods = ["GET", "POST"])
def coachletters():
    if request.method == "GET":
        return render_template('coachletters.html')
    else:
        firstLetter = str(request.form.get("letter"))
        session['firstLetter'] = firstLetter
        return redirect(url_for('coachnames'))

#lists all peoples names with a certain letter
@app.route('/coachnames', methods = ["GET", "POST"])
def coachnames():
    if request.method == "GET":
        firstLetter = session.get("firstLetter")
        Lname = str(firstLetter) + "%"
        coaches = db.engine.execute("SELECT * FROM coaches WHERE Lname LIKE :Lname ORDER BY Lname", Lname = Lname)
        return render_template('coachnames.html', coaches = coaches)
    else:
        return redirect(url_for('coachbio'))

#lists every picture the coach is in
@app.route('/coachbio', methods = ["GET"])
def coachbio():
    coach_ID = int(session.get("coach_ID"))
    coach = Coach.query.filter_by(coach_ID = coach_ID).first()
    #raw SQL to query every photo that the selected coach is in
    #rows = db.engine.execute("SELECT year, filename, sport_name FROM photo_seating INNER JOIN photos on photo_seating.pic_ID = photos.pic_ID INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE coach_ID == :coach_ID", coach_ID = coach_ID)

    return render_template('coachbio.html', coach = coach, rows = rows)

#DONE
@app.route('/sportindex', methods = ["GET", "POST"])
def sportindex():
    #list of all sports
    if request.method == "GET":
        sports = Sport.query.order_by(Sport.sport_name).all()
        return render_template('sportindex.html', sports = sports)
    else:
        sport_ID = int(request.form.get("sport"))
        session['sport_ID'] = sport_ID
        return redirect(url_for('sporthome'))

#DONE
@app.route('/sporthome', methods = ["GET", "POST"])
def sporthome():
    #list of all years of a specific sport
    if request.method == "GET":
        sport_ID = int(session.get("sport_ID"))
        sport = Sport.query.filter_by(sport_ID = sport_ID).first()
        #raw SQL to query every photo of the selected sport
        rows = db.engine.execute("SELECT year, filename, pic_ID FROM photos INNER JOIN sports ON photos.sport_ID = sports.sport_ID WHERE sports.sport_ID == :sport_ID ORDER BY year", sport_ID = sport_ID)
        return render_template('sporthome.html', sport = sport, rows = rows)
    else:
        pic_ID = int(request.form.get("pic-id"))
        session['pic_ID'] = pic_ID
        return redirect(url_for('sportyear'))

#DONE
@app.route('/sportyear', methods = ["GET"])
def sportyear():
    pic_ID = int(session.get("pic_ID"))
    #query database for the photo of a specific sport from a specific year, by photo_ID
    photo = Photo.query.filter_by(pic_ID = pic_ID).first()
    #construct filename
    filename = filename_construct(photo.filename)
    sport_ID = photo.sport_ID
    #query for sport's name
    sport = Sport.query.filter_by(sport_ID = sport_ID).first()
    #query row descriptions
    rows = Row.query.filter_by(pic_ID = pic_ID)
    people_numbers = db.engine.execute("SELECT ath_ID, coach_ID, photo_seating.row_ID FROM photo_seating INNER JOIN rows ON rows.row_ID = photo_seating.row_ID WHERE rows.pic_ID = :pic_ID", pic_ID = pic_ID)
    athletes = []
    for person in people_numbers:
        ath_ID = person.ath_ID
        coach_ID = person.coach_ID
        firstName=""
        lastName=""
        if ath_ID != 0:
            sing_athlete = Athlete.query.filter_by(ath_ID = ath_ID).first()
            firstName = sing_athlete.Fname
            lastName = sing_athlete.Lname
        else:
            sing_coach = Coach.query.filter_by(coach_ID = coach_ID).first()
            if sing_coach != None:
                if str(sing_coach.Fname) == "Coach" or str(sing_coach.Fname) == "coach":
                    firstName = sing_coach.Fname
                else:
                    firstName = "Coach " + str(sing_coach.Fname)
                    lastName = sing_coach.Lname
        r_ID = person.row_ID
        new_person = {"Fname": firstName, "Lname": lastName, "row_ID": r_ID}
        athletes.append(new_person)
    return render_template('sportyear.html', rows = rows, photo = photo, sport = sport, filename = filename, athletes = athletes)

#DONE
@app.route('/yearindex', methods = ["GET", "POST"])
def yearindex():
    if request.method == "GET":
        years = db.engine.execute("SELECT DISTINCT year FROM photos ORDER BY year ASC")
        return render_template('yearindex.html', years = years)
    else:
        year = int(request.form.get("year"))
        session['year'] = year
        return redirect(url_for('yearhome'))

#DONE
@app.route('/yearhome', methods = ["GET", "POST"])
def yearhome():
    if request.method == "GET":
        year = int(session.get("year"))
        #list of pictures before filename is fixed
        initialPictures = db.engine.execute("SELECT sport_name, photos.sport_ID, filename, photos.pic_ID FROM photos INNER JOIN sports on photos.sport_ID = sports.sport_ID WHERE photos.year == :year", year = year)
        #list of pictures after filename is fixed
        updatedPictures = []
        for picture in initialPictures:
            newFilename = filename_construct(picture.filename)
            newPhoto = {"sport_name": picture.sport_name, "sport_ID": picture.sport_ID, "pic_ID": picture.pic_ID, "filename": newFilename}
            updatedPictures.append(newPhoto)
        return render_template('yearhome.html', year = year, pictures = updatedPictures)
    else:
        picture = int(request.form.get("pic_ID"))
        session['pic_ID'] = picture
        return redirect(url_for('sportyear'))

#fix filenames taken from the database
def filename_construct(filename):
    filename = filename.replace('\\', '/')
    filename = filename.replace('E:', '/static/images')
    filename = filename + ".jpg"
    return filename
