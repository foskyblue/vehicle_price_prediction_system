import joblib
import pandas as pd
from sqlalchemy import create_engine


def load_data():
    """
    :return: Data frame
    """
    # load data
    engine = create_engine('sqlite:///data/vehicle_price_prediction.db')
    df = pd.read_sql_table('vehicle_price_prediction', engine)
    return df


def load_model():
    """
    :return: Pickled file used for prediction
    """
    # load model
    model = joblib.load("models/vehicle_price_prediction.pkl")

    return model