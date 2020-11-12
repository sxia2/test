# reference
# https://towardsdatascience.com/deploying-a-keras-deep-learning-model-as-a-web-application-in-p-fc0f2354a7ff

from wtforms import (Form, StringField, validators, SubmitField,
                     DecimalField, IntegerField)
from flask import Flask
from flask import request
from flask import render_template
import message

app = Flask(__name__)

class ReusableForm(Form):
    """User entry form for entering specifics for generation"""
    # Starting seed
    seed = StringField("Enter a seed string or 'random':", validators=[
        validators.InputRequired()])
    # Diversity of predictions
    diversity = DecimalField('Enter diversity:', default=0.8,
                             validators=[validators.InputRequired(),
                                         validators.NumberRange(min=0.5, max=5.0,
                                                                message='Diversity must be between 0.5 and 5.')])
    # Number of words
    words = IntegerField('Enter number of words to generate:',
                         default=50, validators=[validators.InputRequired(),
                                                 validators.NumberRange(min=10, max=100,
                                                                        message='Number of words must be between 10 and 100')])
    # Submit button
    submit = SubmitField("Enter")

# Home page
@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page of app with form"""

    # Create form
    form = ReusableForm(request.form)

    # On form entry and all conditions met
    if request.method == 'POST' and form.validate():
        # Extract information
        seed = request.form['seed']
        diversity = float(request.form['diversity'])
        words = int(request.form['words'])
        # Generate a random sequence
        if seed == 'random':
            return render_template('random.html',
                                   input=message.return_message('random'))
        # Generate starting from a seed sequence
        else:
            return render_template('seeded.html',
                                   input=message.return_message('seeded'))
    # Send template information to index.html
    return render_template('index.html', form=form)

if __name__ == "__main__":
    # Run app
    app.run(host="0.0.0.0", port=80)
