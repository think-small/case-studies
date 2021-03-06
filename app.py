import os
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify, request
from forms import SelectCaseForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedirectory = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "4Lhgnoz8ogcJGtE2tbRNTFsUPqrj7pPRZnzZS9KKqpS293qV8NdeVcvTHmQM"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedirectory, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

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
    history = db.relationship('CaseHistory', backref='case')
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unitID'))

    def __rpr__(self):
        return '<case_unit_mapper %r>' % self.caseID

class CaseTestResults(db.Model):
    __tablename__: "caseTestResults"
    id = db.Column(db.Integer, primary_key=True)
    testName = db.Column(db.String(20), nullable=False)
    lowerBound = db.Column(db.Float(precision = 2), nullable=False)
    upperBound = db.Column(db.Float(precision = 2), nullable=False)
    units = db.Column(db.String(), nullable=False)
    valueType = db.Column(db.String(), nullable=False, default="integer")
    precision = db.Column(db.Integer, nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case_unit_mapper.caseID'))
    def __rpr__(self):
        return '<case_test_results %r>' % self.testName

class NormalTestResults(db.Model):
    __tablename__: "caseTestResults"
    id = db.Column(db.Integer, primary_key=True)
    testName = db.Column(db.String(20), nullable=False)
    lowerBound = db.Column(db.Float(precision = 2), nullable=False)
    upperBound = db.Column(db.Float(precision = 2), nullable=False)
    units = db.Column(db.String(), nullable=False)
    valueType = db.Column(db.String(), nullable=False, default="integer")
    precision = db.Column(db.Integer, nullable=True)
    def __rpr__(self):
        return '<case_test_results %r>' % self.testName

class CaseNotes(db.Model):
    __tablename__: "case_notes"
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(), nullable=False)
    noteType = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)    
    case_id = db.Column(db.Integer, db.ForeignKey('case_unit_mapper.caseID'))
    def __rpr__(self):
        return '<case_notes %r>' % self.note
        
class CaseHistory(db.Model):
    __tablename__: "case_history"
    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    reference = db.Column(db.String(), nullable=True, default = "---")
    reference_name = db.Column(db.String(), nullable=True, default = "---")
    case_id = db.Column(db.Integer, db.ForeignKey('case_unit_mapper.caseID'))
    def __rpr__(self):
        return '<case_history %r>' % self.diagnosis

class UnitsSchema(marshmallow.ModelSchema):
    class Meta:
        fields = ( "unitID", "unit", "mappper" )

    mapper = marshmallow.Nested(CaseUnitMapper)

class CaseHistorySchema(marshmallow.ModelSchema):
    class Meta:
        model = CaseHistory
    
class CaseTestResultsSchema(marshmallow.ModelSchema):
    class Meta:
        model = CaseTestResults

class NormalTestResultsSchema(marshmallow.ModelSchema):
    class Meta:
        model = NormalTestResults

class CaseNotesSchema(marshmallow.ModelSchema):
    class Meta:
        model = CaseNotes

class CaseUnitMapperSchema(marshmallow.Schema):
    class Meta:
        fields = ('caseID', 'unitID', 'testResults', 'notes', 'history')

    testResults = marshmallow.Nested(CaseTestResultsSchema, many=True)
    notes = marshmallow.Nested(CaseNotesSchema, many=True)
    history = marshmallow.Nested(CaseHistorySchema, many=True)

@app.route("/", methods=["GET", "POST"])
def index():
    #  Clear session keys
    key_list = list(session.keys())
    for key in key_list:
        session.pop(key)

    form = SelectCaseForm()
    if 'selected_case' in session.keys():
        return redirect( url_for("transcripts", form = form, case = session['selected_case'], unit_name = session['unit_name']) )
    return render_template("index.html", form = form)

@app.route("/get_cases", methods = ["POST"])
def get_cases():
    form = SelectCaseForm()

    query = CaseUnitMapper.query.filter_by(unitID = 1).all()
    mapper_schema = CaseUnitMapperSchema(many=True)
    # TODO: randomize queried cases
    session['cases'] = mapper_schema.dump(query)
    session['selected_case'] = session['cases'][0]

    unit_name_query = Units.query.filter_by(unitID = session['selected_case']['unitID']).first()
    units_schema = UnitsSchema()
    session['unit_name'] = units_schema.dump(unit_name_query)['unit']

    return redirect( url_for("transcripts", form = form) )

@app.route("/trancripts", methods = ["GET", "POST"])
def transcripts():
    form = SelectCaseForm()
    if 'selected_case' not in session.keys():
        return redirect( url_for("index") )
    return render_template("transcripts.html", form = form, case = session['selected_case'], unit_name = session['unit_name'])

@app.route("/history", methods = ["GET"])
def history():
    form = SelectCaseForm()
    if 'selected_case' not in session.keys():
        return redirect( url_for("index") )
    return render_template("history.html", form = form, case = session['selected_case'], unit_name = session['unit_name'])

@app.route("/orders", methods = ["GET", "POST"])
def orders():
    if 'selected_case' not in session.keys():
        return redirect( url_for("index") )
    form = SelectCaseForm()
    normal_results_query = NormalTestResults.query.all()
    normal_results_schema = NormalTestResultsSchema(many=True)
    normal_results = normal_results_schema.dump(normal_results_query)
    return render_template("orders.html", form = form, case = session['selected_case'], unit_name = session['unit_name'], normal_results = normal_results)

if __name__ == "__main__":
    app.run(debug = True)