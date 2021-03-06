from flask import Flask, request, session, render_template, abort, redirect, url_for
from models import db, User, Waveform, UserTracker
import datetime
import os
import sys
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.root_path, "audioboard.db"
)
# Suppress deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    if "username" in session:
        waveforms = None
        user = User.query.filter_by(username=session['username']).first()
        if user.waveforms:
            waveforms = user.waveforms
        return render_template("landing.html", user=user, waveforms=waveforms)
    return render_template("landing.html", user=None, waveforms=None)


@app.route('/register/', methods=['GET', 'POST'])
def registrar(error=None):
    if 'logged_in' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if not request.form['username']:
            error = 'Please Enter a Username'
        elif not request.form['password']:
            error = 'Please Enter a Password'
        elif request.form['password'] != request.form['password2']:
            error = 'Passwords Dont Match'
        elif User.query.filter_by(username=request.form['username']).first() is not None:
            error = 'Username Taken'
        else:
            db.session.add(
               User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return render_template('registeredPage.html')
    return render_template('register.html', error=error)


@app.route('/waveforms/', methods=['GET', 'POST'])
def send_waveform(): #may not allow for extraneous posts, may have to remove user check
    prediction = None
    username=None
    if request.method == 'POST':
        prediction = request.form['prediction']
        t = UserTracker.query.filter_by(id=1).first()
        username = t.current
        u = User.query.filter_by(username=username).first()
        w = Waveform(user_id=u.id, success=True, prediction=prediction, time=datetime.datetime.now())
        db.session.add(w)
        db.session.commit()
        u.current_waveform_id = w.id
        db.session.commit()
        print(u.current_waveform_id, file=sys.stderr)
        return render_template('analyze.html', prediction=prediction, username=username), 201
    return render_template('analyze.html', prediction=prediction)


@app.route('/predictions/', methods=['GET', 'POST'])
def predict():  # may not allow for extraneous posts, may have to remove user check
    if 'username' in session:
        new = None
        prediction = None
        error = None
        current = None
        m = UserTracker.query.filter_by(id=1).first()
        u = User.query.filter_by(username=m.current).first()
        current = u.current_waveform_id
        w = Waveform.query.filter_by(id=current).first()
        index = 0
        waveforms = u.waveforms
        for w in waveforms:
            index += 1
            if w.id == current:
                break
        if w:
            prediction = w.prediction
        if request.method == 'POST':
            # update current_wave_for_id
            update = str(request.form['success'])
            u = User.query.filter_by(username=session['username']).first()  # get user and update waveform data
            target = u.current_waveform_id
            w = Waveform.query.filter_by(id=target).first()
            index = 0
            waveforms = u.waveforms
            for w in waveforms:
                index += 1
                if w.id == current:
                    break
            if update == 'no':
                w.success = False
                db.session.commit()
            else:
                w.success = True
                db.session.commit()
            error = "Waveform status updated"
            return render_template('analyze.html', new='True', error=error, prediction=prediction,index = index), 201
        return render_template('analyze.html', prediction=prediction, current=current, new=new, error=error, index=index)
    else:
        return abort(404)

#make a POST to server to give username

@app.route("/login/", methods=["GET", "POST"])
def logger():
    #get a list of all active usernames
    # first check if the user is already logged in
    success = None
    if "username" in session:
        return redirect(url_for("home"))
    error = None
    # if not, and the incoming request is via POST try to log them in
    if request.method == "POST":
        u = User.query.filter_by(username=request.form['username']).first()
        if u is None:
            error = 'invalid username'
        else:
            if u.password != request.form["password"]:
                error = 'invalid password'
            else:
                session['logged_in'] = True
                session["username"] = request.form["username"]
                m = UserTracker.query.filter_by(id=1).first()
                m.current = request.form["username"]
                db.session.commit()
                return render_template("loggedInPage.html")
        # if all else fails, offer to log them in
    return render_template("loginPage.html", error=error)


@app.route("/successes/")
def tracker():
    if "username" in session:
        success = 0.0
        num = 0
        percent = 0
        u = User.query.filter_by(username=session["username"]).first()
        if u.waveforms is not None:
            for w in u.waveforms:
                if w.success is True:
                    success += 1.00
                num += 1.00
            if num != 0:
                percent = success/num*100
                num = num/1
            return render_template("success_rate.html", percent=percent, num=num, waveforms=u.waveforms)
        else:
            return render_template("success_rate.html", percent=None, num=None)
    else:
        return abort(404)


@app.route("/logout/")
def unlogger():
    # if logged in, log out, otherwise offer to log in
    if "username" in session:
        session.clear()
        return render_template("logoutPage.html")
    else:
        return redirect(url_for("logger"))



# CLI Commands
@app.cli.command("initdb")
def init_db():
    """Initializes database and any model objects necessary for assignment"""
    db.drop_all()
    db.create_all()
    current = UserTracker()
    db.session.add(current)
    db.session.commit()
    print("Initialized AudioBoard DB.")


@app.cli.command("devinit")
def init_dev_data():
    """Initializes database with data for development and testing"""
    db.drop_all()
    db.create_all()
    print("Initialized AudioBoard DB.")



    u1 = User(username="nigel", password="pass")
    u2 = User(username="harry", password="pass")
    current = UserTracker()

    db.session.add(u1)
    print("Created %s" % u1.username)
    db.session.add(u2)
    print("Created %s" % u2.username)
    db.session.add(current)

    db.session.commit()
    print("Added dummy data.")


# needed to use sessions
# note that this is a terrible secret key
app.secret_key = "this is a terrible secret key"


if __name__ == "__main__":
    app.run(threaded=True)
