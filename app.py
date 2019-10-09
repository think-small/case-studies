import os
from flask import Flask, render_template, session, redirect, url_for, flash
from forms import SelectCaseForm
from flask_sqlalchemy import SQLAlchemy

basedirectory = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "4Lhgnoz8ogcJGtE2tbRNTFsUPqrj7pPRZnzZS9KKqpS293qV8NdeVcvTHmQM"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedirectory, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Units(db.Model):
    __tablename__: "units"
    unitID = db.Column(db.Integer, primary_key=True)
    unit = db.Column(db.String(64), nullable=False)
    mapper = db.relationship('CaseUnitMapper', backref='unit')

    def __rpr__(self):
        return '<Unit %r>' % self.unit

class CaseUnitMapper(db.Model):
    __tablename__: "case_unit_mapper"
    caseID = db.Column(db.Integer, primary_key=True)
    unitID = db.Column(db.Integer, nullable=False)
    testResults = db.relationship('CaseTestResults', backref='case')
    notes = db.relationship('CaseNotes', backref='case')
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unitID'))

    def __rpr__(self):
        return '<case_unit_mapper %r>' % self.caseID

class CaseTestResults(db.Model):
    __tablename__: "caseTestResults"
    id = db.Column(db.Integer, primary_key=True)
    testName = db.Column(db.String(20), nullable=False)
    lowerBound = db.Column(db.Integer, nullable=False)
    upperBound = db.Column(db.Integer, nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case_unit_mapper.caseID'))
    def __rpr__(self):
        return '<case_test_results %r>' % self.testName

class CaseNotes(db.Model):
    __tablename__: "case_notes"
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(), nullable=False)
    noteType = db.Column(db.String(), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('case_unit_mapper.caseID'))
    def __rpr__(self):
        return '<case_notes %r>' % self.note

@app.route("/", methods=["GET", "POST"])
def index():
    form = SelectCaseForm()
    if form.validate_on_submit():
        session['units'] = {
            'osmo': form.osmoLytes.data,
            'renal': form.renal.data,
            'lipids': form.lipoprotein.data,
            'hepatitisHiv': form.hepatitisHiv.data,
            'enzymes': form.enzymes.data
        }

        session['unitsMapper'] = {
            'osmo': 1,
            'renal': 2,
            'lipids': 3,
            'hepatitisHiv': 4,
            'enzymes': 5
        }

        units_to_query = []
        for key, value in session['units'].items():
            if value:
                units_to_query.append(session['unitsMapper'][key])
        
        queried_cases = []
        for value in units_to_query:
            query = CaseUnitMapper.query.filter_by(unitID = value).all()
            queried_cases.append(query)
        session['cases'] = queried_cases
        session['selected_case'] = session['cases'][0][0]
        session['selected_case_notes'] = []
        for note in session['selected_case'].notes:
            session['selected_case_notes'].append([note.note, note.noteType])

        if all( value == False for value in session['units'].values() ):
            flash('Choose at least one unit to review')
            return redirect( url_for('index') )
        else:
            flash('New case loaded!')
            return redirect( url_for('transcripts') )
    return render_template("index.html", form = form)

@app.route("/trancripts", methods = ["GET", "POST"])
def transcripts():
    form = SelectCaseForm()
    notes = session['selected_case_notes']
    return render_template("transcripts.html", form = form, notes = notes)

if __name__ == "__main__":
    app.run(debug = True)