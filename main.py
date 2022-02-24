from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from train_validation import TrainValidation
from train_model import TrainModel
from predict_results import PredictResults
from prediction_validation import PredictionValidation
from Dataframe_to_Image.df_to_image import df_to_image
import os
from wsgiref import simple_server


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'


class InfoForm(FlaskForm):
    cement = StringField('What is the amount of Cement? in kg/m3: ', validators=[DataRequired()])
    blast_furnace_slag = StringField('What is the amount of Blast Furnace Slag? in kg/m3: ', validators=[DataRequired()])
    fly_ash = StringField('What is the amount of Fly Ash? in kg/m3: ', validators=[DataRequired()])
    water = StringField('What is the amount of Water? in kg/m3: ', validators=[DataRequired()])
    super_plasticizer = StringField('What is the amount of Super Plasticizer? in kg/m3: ', validators=[DataRequired()])
    coarse_aggregate = StringField('What is the amount of Coarse Aggregate? in kg/m3: ', validators=[DataRequired()])
    fine_aggregate = StringField('What is the amount of Fine Aggregate? in kg/m3: ', validators=[DataRequired()])
    age = StringField('What is the Age of Concrete? in days: ', validators=[DataRequired()])
    submit = SubmitField('Predict')


class PredictionFolderForm(FlaskForm):
    location = StringField("Enter the location/path of the batch files for prediction: ", validators=[DataRequired()])
    submit = SubmitField("Start Prediction")


class TrainingFolderForm(FlaskForm):
    location = StringField("Enter the location/path of the batch files for training: ", validators=[DataRequired()])
    submit = SubmitField("Start Training")


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/train", methods=["GET", "POST"])
def train():
    form = TrainingFolderForm()
    show = False
    if form.validate_on_submit():
        show = True
        session['location'] = form.location.data
        validation = TrainValidation(session['location'])
        try:
            validation.train_validation()
            train = TrainModel()
            train.model_training()
            trained = True
        except:
            trained = False

        if trained:
            flash("Training Successful!")
        else:
            flash(f"No files/valid files are present in the {session['location']} for training.")
    form.location.data = ''
    return render_template('train.html', form=form, show=show)


@app.route('/predict_one', methods=['GET', 'POST'])
def predict_one():
    form = InfoForm()
    show = False
    if form.validate_on_submit():
        show = True
        session['cement'] = float(form.cement.data)
        session['blast_furnace_slag'] = float(form.blast_furnace_slag.data)
        session['fly_ash'] = float(form.fly_ash.data)
        session['water'] = float(form.water.data)
        session['super_plasticizer'] = float(form.super_plasticizer.data)
        session['coarse_aggregate'] = float(form.coarse_aggregate.data)
        session['fine_aggregate'] = float(form.fine_aggregate.data)
        session['age'] = float(form.age.data)
        predict = PredictResults("Prediction_Batch_Files")
        result = predict.predict_one([session['cement'], session['blast_furnace_slag'], session['fly_ash'], session['water'], session['super_plasticizer'], session['coarse_aggregate'], session['fine_aggregate'], session['age']])
        result = round(result, 2)
        flash(f"{result:0.2f} MPa")
        return redirect(url_for('predict_one'))
    form.cement.data = ''
    form.blast_furnace_slag.data = ''
    form.fly_ash.data = ''
    form.water.data = ''
    form.super_plasticizer.data = ''
    form.coarse_aggregate.data = ''
    form.fine_aggregate.data = ''
    form.age.data = ''
    return render_template('predict_one.html', form=form, show=show)


@app.route("/predict_many", methods=["GET", "POST"])
def predict_many():
    form = PredictionFolderForm()
    show = False
    if form.validate_on_submit():
        show = True
        session['location'] = form.location.data
        validation = PredictionValidation(session['location'])
        try:
            validation.prediction_validation()
            predict = PredictResults(session['location'])
            df = predict.predict_many()
            df_to_image(df, 'dataframe', rows=5)
            validated = True
        except:
            validated = False

        if validated:
            flash("Prediction Successful!")
        else:
            flash(f"No files/valid files are present in the {session['location']}.")
    form.location.data = ''
    return render_template("predict_many.html", form=form, show=show)


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


port = int(os.getenv("PORT",5000))
if __name__ == "__main__":
    host = '0.0.0.0'
    # port = 5000
    httpd = simple_server.make_server(host, port, app)
    print("Serving on %s %d" % (host, port))
    httpd.serve_forever()
