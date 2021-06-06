### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Analysis & Results](#analysis&results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

To run this project, you can clone this repository onto your local machine and follow the instructions below to run locally. Also, you can access the web app [here]().

The version of python used is python 3.8.8. 

Other libraries needed to successfully run this project includes:

1. Pandas
2. Numpy
3. Matplotlib
4. Plotly
5. Flask
6. Sqlite3
7. Nltk

Also, you can use the requirements.txt file above.

#### To run the project locally:

1. Clone the repo to your local machine
2. Navigate to the root folder.
3. Run the command below to clean the data and save to an sqlite3 database file: 
   
   ```
   python data/process_data.py data/cars.csv data/trucks.csv data/vehicle_price_prediction.db 
   ```

4. Run the command to train a classifier and save the results to a pickle file.: 
   
   ```
   python models/train_classifier.py data/disaster_response.db models/disaster_response_pickle.pkl 
   ```

5. Run the command to start the web app locally:

    ```
    python app/run.py
    ```

## Project Motivation<a name="motivation"></a>

There are thousands of vehicles being sold locally each day in Nigeria. However, there's no way to tell if the vehicle that one is about to purchase is really worth the price. This motivated me to build a model that will assist both potential buyers and sellers to estimate the cost of a vehicle based on some well known features.  


## File Descriptions <a name="files"></a>

This project is made up of 3 folders, app, data and models.

* app
    * templates
        * go.html - prediction result template
        * master.html - index template
    * figures.py - plots using Plotly
    * load.py - responsible for loading sqlite3 database, dataframe and pickle files
    * run.py - main program

* data
    * cars.csv - cars listed for sale on the Autochek [website](https://autochek.africa/ng)
    * trucks.csv - trucks listed for sale on the Autochek [website](https://autochek.africa/ng)
    * vehicle_price_prediction.db - saved sqlite3 database file
    * process_data.py - data ETL pipeline
    
* models
    * vehicle_price_prediction.pkl - saved pickle file that will be used for prediction
    * train_classifier.py - train machine learning model


Other files included will be for deploying the web app to the Heroku cloud service.

## Analysis & Results <a name="analysis&results"></a>

An extensive data analysis and all the results can be seen in the jupyter notebook file: vehicle_price_prediction.ipynb
 

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

All credit goes to [Autochek Nigeria](https://autochek.africa/ng) for the data and [Udacity](https://www.udacity.com/) for the immense help and motivation in completing this project.
