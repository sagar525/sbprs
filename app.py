# This is basically the heart of my flask
from flask import Flask, render_template, request
from model import RecommendationSystem
import warnings

warnings.filterwarnings("ignore")

#initialize flask application
app = Flask(__name__)  # intitialize the flaks app  # common

#get the recommendation object
recommendation_system = RecommendationSystem()


@app.route('/', methods=['GET', 'POST'])
def recommend_products():

    #This var contains the items from the recommendation system
    items = ""

    #to indicate if we just started the application
    start = True

    #if method is post then check for username and return items
    if request.method == 'POST':

        items = recommendation_system.recommend_products(request.form['username'])

        if items is None:
            return render_template('index.html', items=None, flag=False, start=False)
        else:
            return render_template('index.html',username=request.form['username'], items=items, flag=True,start=False)
    else:
        return render_template('index.html', items=None, flag=False, start=True)


# Any HTML template in Flask App render_template

if __name__ == '__main__':
    app.run(debug=True)  # this command will enable the run of your flask app or api

    # ,host="0.0.0.0")
