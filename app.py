from flask import Flask, render_template, session, redirect, url_for, flash
from forms import SelectCaseForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "4Lhgnoz8ogcJGtE2tbRNTFsUPqrj7pPRZnzZS9KKqpS293qV8NdeVcvTHmQM"

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
        if all( value == False for value in session['units'].values() ):
            flash('Choose at least one unit to review')
            return redirect( url_for('index') )
        else:
            flash('New case loaded!')
            return redirect( url_for('index') )
    return render_template("index.html", form = form)

if __name__ == "__main__":
    app.run(debug = True)