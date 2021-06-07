import sys
import numpy as np
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score

import pickle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def load_data(database_filepath):
    """
    :param database_filepath: file path of data to be loaded
    :return: training data dataframe, target columns dataframe and target column names
    """
    engine = sqlite3.connect(database_filepath)
    df = pd.read_sql("SELECT * FROM vehicle_price_prediction", engine)
    Y = df['marketplacePrice']
    X = df.drop('marketplacePrice', axis=1)

    return X, Y


def build_model():
    """
    :param : None
    :return: Grid search model pipeline
    """
    pipeline = Pipeline([
        # ('clf', RandomForestRegressor())
        ('clf', RandomForestRegressor(n_estimators = 300, random_state = 42))
        # RandomForestClassifier(random_state = 42)
    ])

    parameters = {
        # "clf": [RandomForestRegressor()],
        # "n_estimators": [100],
        # 'random_state': [14],
    }
    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv


def evaluate_model(model, X_test, Y_test, X_train, Y_train):
    """
    :param model: Grid search model pipeline to be used for prediction and evaluation
    :param X_test: test data sets
    :param Y_test: test data sets target columns to evaluate classifier
    :param category_names: test data column names
    :return: None
    """
    cv = 5 # Cross  Validation value
    r_2 = [] # r2 scores list
    CV = [] # Cross Validation scores mean list

    y_pred_cv = model.predict(X_test)
    Y_test = np.array(Y_test)

    y_pred_cv = pd.DataFrame(y_pred_cv)
    r_squared = r2_score(Y_test, y_pred_cv)
    cross_val = cross_val_score(model, X_train, Y_train, cv=cv)

    print(model,"\n") 
    print("r_2 score: ",r_squared,"\n")
    print("CV scores: ",cross_val,"\n")
    print("CV scores mean: ",cross_val.mean())


def save_model(model, model_filepath):
    """
    :param model: Grid search model pipeline
    :param model_filepath: file path where model will be saved
    :return: None
    """
    pkl_filename = model_filepath
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y = load_data(database_filepath)
        x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(x_train, y_train)

        print('Evaluating model...')
        evaluate_model(model, x_test, y_test, x_train, y_train)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database ' \
              'as the first argument and the filepath of the pickle file to ' \
              'save the model to as the second argument. \n\nExample: python ' \
              'train_classifier.py ../data/vehicle_price_prediction.db vehicle_price_prediction.pkl')


if __name__ == '__main__':
    main()