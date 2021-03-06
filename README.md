### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Analysis & Results](#analysis&results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

To run this project, you can clone this repository onto your local machine and follow the instructions below to run locally. Also, you can access the web app [here](https://naija-vehicle-price-prediction.herokuapp.com/).

The version of python used is python 3.8.8. 

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
   python models/train_classifier.py data/vehicle_price_prediction.db models/vehicle_price_prediction.pkl 
   ```

5. Run the command to start the web app locally:

    ```
    python app.py
    ```
Then access the web app locally via: http://127.0.0.1:5000/

## Project Motivation<a name="motivation"></a>

There are thousands of vehicles being sold locally each day in Nigeria. However, there's no way to tell if the vehicle that one is about to purchase is really worth the price. This motivated me to build a model that will assist both potential buyers and sellers to estimate the cost of a vehicle based on some well known features.  


## File Descriptions <a name="files"></a>

This project is made up of 2 folders, app, data and models.

We have the following files/folder in the root folder

* templates
    * go.html - prediction result template
    * master.html - index template
* figures.py - plots using Plotly
* load.py - responsible for loading sqlite3 database, dataframe and pickle files
* Recommender.py - a knowledge based recommender engine class
* run.py - main program
* Procfile - heroku deployment file
* requirements.txt - requirements file for heroku
* runtime.txt - heroku deployment file
* vehicle_price_prediction.ipynb - jupyter notebook file

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

![index1](https://user-images.githubusercontent.com/16907846/120944069-804cc200-c72a-11eb-8098-dc479d4bdc8b.JPG)
![index2](https://user-images.githubusercontent.com/16907846/120944075-8347b280-c72a-11eb-968e-e71b70681f3a.JPG)
![index3](https://user-images.githubusercontent.com/16907846/120944139-c99d1180-c72a-11eb-9044-00c2804d64dd.JPG)


## Licensing, Authors, Acknowledgements<a name="licensing"></a>

All credit goes to [Autochek Nigeria](https://autochek.africa/ng) for the data and [Udacity](https://www.udacity.com/) for the immense help and motivation in completing this project.
