import sys
import pandas as pd
import sqlite3
import warnings
warnings.filterwarnings("ignore")
from sqlalchemy import create_engine


def load_data(cars_filepath, trucks_filepath):
    """
    :param messages_filepath: file path for messages file in csv format
    :param categories_filepath: file path for message categories file in csv format
    :return: merged message and categories dataframe
    """
    # read data
    cars = pd.read_csv(cars_filepath)
    trucks = pd.read_csv(trucks_filepath)

    # merge both data sets
    df = pd.concat([cars, trucks], ignore_index=True) # pd.merge(cars, trucks)
    return df


def clean_data(df):
    """
    :param df: merged message and categories dataframe
    :return: cleaned dataframe
    """
    df.drop(df.columns[df.isna().sum()/df.shape[0] > .9].tolist(), axis=1, inplace=True)

    columns_to_be_dropped = ['id', 'vin', 'licensePlate', 'createdBy', 'marketplaceVisibleDate', 
                            'ownerId', 'country', 'address', 'state', 'carManagerId', 'city', 
                            'createdAt', 'hasWarranty', 'loanValue', 'websiteUrl', 'installment', 
                            'insured', 'marketplaceVisible', 'ownerType', 'depositReceived', 
                            'hasThreeDImage', 'price', 'marketplaceOldPrice']

    df = df.drop(columns_to_be_dropped, axis=1)

    # Handling outliers

    Q1 = df[['year', 'mileage', 'marketplacePrice', 'gradeScore']].quantile(0.25)
    Q3 = df[['year', 'mileage', 'marketplacePrice', 'gradeScore']].quantile(0.75)
    IQR = Q3 - Q1

    df = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]

    df['model_name'] = df['model_name'].apply(lambda row: row.strip().lower())
    df['model_brand_name'] = df['model_brand_name'].apply(lambda row: row.strip().lower())
    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.strip().lower())
    df['exteriorColor'] = df['exteriorColor'].apply(lambda row: row.strip().lower())
    df['bodyType'] = df['bodyType'].apply(lambda row: row.strip().lower())
    df['engineType'] = df['engineType'].apply(lambda row: row.strip().lower())
    df['isFirstOwner'] = df['isFirstOwner'].astype(str).apply(lambda row: row.strip().lower())

    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.replace('and', '&'))
    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.replace('ad', '&'))
    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.replace('/', ' & '))
    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.replace('off white', 'off-white'))
    df['interiorColor'] = df['interiorColor'].apply(lambda row: row.replace('off- white', 'off-white'))

    df['exteriorColor'] = df['exteriorColor'].apply(lambda row: row.replace('and', '&'))
    df['exteriorColor'] = df['exteriorColor'].apply(lambda row: row.replace('ad', '&'))
    df['exteriorColor'] = df['exteriorColor'].apply(lambda row: row.replace('/', ' & '))

    colors_replacement = {'ash colour': 'ash', 'ash mixed with grey color': 'ash & grey',
                      'ashley': 'ash', 'beige': 'biege', 'biege & black': 'biege & black',
                      'black & beige': 'biege & black', 'black on brown': 'black & brown',
                      'brown & black': 'black & brown', 'creame': 'cream', 'crean': 'cream',
                      'creme': 'cream', 'cream colour': 'cream', 'dark ash': 'ash', 'dark blue': 'blue',
                      'dark blue & grey': 'blue & grey', 'dark green': 'green',
                      'dark grey': 'grey', 'dark grey & blue': 'blue & grey', 
                      'dotted black grey': 'grey', 'grey & ash': 'ash & grey', 'gray': 'grey', 'grey & black': 'black & grey',
                      'grey & blue': 'blue & grey', 'grey & dark grey': 'grey', 'ivort': 'ivory',
                      'light  brown': 'brown', 'light brown': 'brown', 'light grey': 'grey',
                      'milk': 'white', 'milk & black': 'white & black', 'milk & chocolate': 'white & brown',
                      'milk color': 'white', 'milk colour': 'white', 'parchment colour': 'parchment', 'red & black': 'black & red',
                      'wine': 'red'}

    df['interiorColor'] = df['interiorColor'].apply(lambda row: colors_replacement[row] if \
                                              row in colors_replacement.keys() else row)



    # save csv to clean form
    print('Saving dataframe to clean.csv...')
    df.drop(['marketplacePrice', 'exteriorColor'], axis=1).to_csv("data/clean.csv", index=False)

    df['isFirstOwnerDummy'] = pd.get_dummies(df['isFirstOwner'], drop_first=True)
    df['transmissionDummy'] = pd.get_dummies(df['transmission'], drop_first=True)
    df['fuelTypeDummy']= pd.get_dummies(df['fuelType'], drop_first=True)
    df['mileageUnitDummy'] = pd.get_dummies(df['mileageUnit'], drop_first=True)
    df.drop(['isFirstOwner', 'transmission', 'fuelType', 'mileageUnit', 'exteriorColor'], axis=1, inplace=True)

    # save csv to html table
    print('Saving dataframe to html table...')
    df.to_html("templates/html_table.html")

    df = pd.get_dummies(df)
    
    return df


def save_data(df, database_filename):
    """
    :param df: cleaned dataframe
    :param database_filename: name of database when saved
    :return: None
    """
    if '.' in database_filename:
        database_filename = database_filename.split('.')[0]
    
    engine = create_engine('sqlite:///'+database_filename+'.db')
    table_name = database_filename.split('/')[1]
    df.to_sql(table_name, engine, index=False, if_exists="replace")


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    CARS: {}\n    TRUCKS: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the car and truck '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'cars.csv trucks.csv '\
              'vehicle_price_prediction.db')


if __name__ == '__main__':
    main()