from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    waveforms = db.relationship("Waveform", backref="user", lazy="joined")
    current_waveform_id = db.Column(db.Integer)


class Waveform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    success = db.Column(db.Boolean, nullable=False, default=True)
    prediction = db.Column(db.String(100), nullable=False)
    time = db.Column(db.Date, nullable=False)

    def to_string(self):
        return "Your #%s waveform on %s predicted to be \"%s\": %s" % (str(self.id), str(self.time), self.prediction, self.success)

