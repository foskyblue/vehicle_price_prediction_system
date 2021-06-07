import json
from Recommender import RecommendationEngine
from numpy import unique
import plotly
import pandas as pd


from flask import Flask
from flask import render_template, request, jsonify
from plotly.graph_objs import Bar
from sqlalchemy import create_engine
from load import load_data, load_model
from figures import load_figures


app = Flask(__name__)

# load data
df = load_data()


# load model
model = load_model()


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    # load figures and ids
    ids, graph_json = load_figures()
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graph_json)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    # query = request.args.get('query', '')

    model_brand_name = [request.args.get('model_brand_name', '')]
    model_name = [request.args.get('model_name', '')]
    year = [int(request.args.get('year', ''))]
    transmission = [request.args.get('transmission', '')]
    engine_type = [request.args.get('engine_type', '')]
    body_type = [request.args.get('body_type', '')]
    mileage = [int(request.args.get('mileage', ''))]
    mileage_unit = [request.args.get('mileage_unit', '')]
    fuel_type = [request.args.get('fuel_type', '')]
    grade_score = [float(request.args.get('grade_score', ''))]
    first_owner = [request.args.get('first_owner', '')]
    selling_condition = [request.args.get('selling_condition', '')]
    interior_color = [request.args.get('interior_color', '')]
    # exterior_color = [request.args.get('exterior_color', '')]

    query = "Make: ", model_brand_name, '\n' " Model: ", model_name, "\n year: ", year, \
            "\n Transmission: ", transmission, "\n Engine Type: ", engine_type, \
            "\n Body Type: ", body_type  

    pred_df = {'year': year, 'mileage': mileage, 'model_name': model_name, 'model_brand_name': model_brand_name,
               'transmission': transmission, 'fuelType': fuel_type, 'sellingCondition': selling_condition,
               'bodyType': body_type, 'mileageUnit': mileage_unit, 'interiorColor': interior_color,
               'engineType': engine_type, 'gradeScore': grade_score, 'isFirstOwner': first_owner
              }

    pred_df = pd.DataFrame(pred_df)

    pred_df['model_name'] = pred_df['model_name'].apply(lambda row: row.strip().lower())
    pred_df['model_brand_name'] = pred_df['model_brand_name'].apply(lambda row: row.strip().lower())
    pred_df['interiorColor'] = pred_df['interiorColor'].apply(lambda row: row.strip().lower())
    pred_df['bodyType'] = pred_df['bodyType'].apply(lambda row: row.strip().lower())
    pred_df['engineType'] = pred_df['engineType'].apply(lambda row: row.strip().lower())
    pred_df['isFirstOwner'] = pred_df['isFirstOwner'].apply(lambda row: row.strip().lower())


    x_clean_pd = pd.read_csv('data/clean.csv')

    to_pred = pd.concat([x_clean_pd, pred_df], ignore_index=True)


    to_pred['isFirstOwnerDummy'] = pd.get_dummies(to_pred['isFirstOwner'].astype(str).apply(lambda row: row.strip().lower()), drop_first=True)
    
    to_pred['transmissionDummy'] = pd.get_dummies(to_pred['transmission'], drop_first=True)

    to_pred['fuelTypeDummy'] = pd.get_dummies(to_pred['fuelType'].astype(str), drop_first=True)
    
    to_pred['mileageUnitDummy'] = pd.get_dummies(to_pred['mileageUnit'].astype(str), drop_first=True)

    to_pred.drop(['isFirstOwner', 'transmission', 'fuelType', 'mileageUnit'], axis=1, inplace=True)

    to_pred = pd.get_dummies(to_pred)
    
    _pred = to_pred.loc[to_pred.shape[0] - 1]
    
    pred_price = model.predict(_pred.values.reshape(1, -1))

    cars_df = pd.read_csv('data/cars.csv')
    trucks_df = pd.read_csv('data/trucks.csv')

    vehicles_df = pd.concat([cars_df, trucks_df], ignore_index=True)

    # convert values to lower case
    # vehicles_df_dtypes = list(vehicles_df.dtypes[(vehicles_df.dtypes == object)].index)
    vehicles_df_dtypes = ['model_name', 'model_brand_name', 'transmission', 'fuelType', 'sellingCondition', 'bodyType', 'engineType']

    for t in vehicles_df_dtypes:
        vehicles_df[t] = vehicles_df[t].apply(lambda row: row.lower())

    recommender_engine = RecommendationEngine()

    recommendations = recommender_engine.get_recommendations(vehicles_df, model_name[0], model_brand_name[0], year[0], body_type[0])

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        pred_df="{:,}".format(round(pred_price[0])),
        recommendations=recommendations
    )


@app.route('/html_table')
def html_table():
    return render_template('html_table.html')


def main():
    app.run()


if __name__ == '__main__':
    main()