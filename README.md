# sqlalchemy-challenge
## SQLAlchemy Project

### Overview
This project involves working with SQLAlchemy to interact with a SQLite database containing weather data. The tasks include setting up the database, reflecting tables, defining ORM classes, querying data, performing analysis, and visualizing results using Pandas and Matplotlib.

### Project Objectives
The primary objectives of this project are:

- Set up a SQLite database and reflect existing tables.
- Define ORM classes to interact with database tables.
- Query and analyze weather data using SQLAlchemy queries.
- Visualize data using Pandas and Matplotlib for insights.

### Project Structure
Step-by-Step Process:
- Database Setup and Reflection
- Create a SQLite database and establish an engine.
- Reflect existing tables (measurement and station).
- Use Flask api

### Part: 1 Define ORM Classes
- Define classes Measurement and Station using SQLAlchemy ORM.
- Map these classes to the reflected tables.

### Querying and Analysis

- Perform various queries to analyze the data:
- Retrieve the last 12 months of precipitation data.
- Calculate summary statistics for precipitation data.
- Find the most active stations.
- Query temperature data for the most active station.
- Visualize temperature data using histograms.
- Data Visualization

### Use Pandas and Matplotlib to visualize:
- Precipitation data over time.
- Temperature distribution at the most active station.
- Summary statistics of precipitation data.

Closing Session - This is an important step.
Close the SQLAlchemy session to finalize operations in your script.

The files included for this Project in the GitHub Repository:
sqlalchemy_analysis.ipynb: Jupyter notebook containing the SQLAlchemy analysis and visualization code.
Resources/: Directory containing CSV files (hawaii_measurements.csv and hawaii_stations.csv) used to populate the database.
Output/: Directory for storing generated plots and visualizations.

## Instructions for Running the Code
To run the project:
Clone the repository to your local machine.
Ensure Python, Jupyter Notebook, and necessary libraries (including SQLAlchemy, Pandas, and Matplotlib) are installed.
Open and execute sqlalchemy_analysis.ipynb in Jupyter Notebook.
Follow the step-by-step instructions and code blocks within the notebook to execute queries, analyze data, and visualize results.

### Part 2: Flask API Implementation
Tip:
- Create Virtual Environment to create the python script
- Ensure Virtual Environment is in same directory as python script
- 
- Create app.py and add the following code:

python
Copy code
# Import the dependencies.
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

#################################################
# Database Setup
#################################################
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hawaii.sqlite"
db = SQLAlchemy(app)

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# Reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=db.engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year ago from the last data point in the database
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query for the dates and precipitation values in the last year
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    results = session.query(Station.station).all()

    # Convert list of tuples into a normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year ago from the last data point in the database
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the most active station
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).first()[0]

    # Query the dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert list of tuples into a list of dictionaries
    tobs_list = [{date: tobs} for date, tobs in results]

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_range(start, end=None):
    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    # Convert the result into a list
    temps = list(np.ravel(results))

    return jsonify(temps)

if __name__ == '__main__':
    app.run(debug=True)
Ensure your virtual environment is activated:

Copy code
source venv/bin/activate
Run the Flask application:

Copy code
python app.py
Access the API:
Open a web browser and go to http://127.0.0.1:5000/ to access the API home page. The available routes will be listed.

### Credits
- Class Notes
- Peer Discussions
- Stack Overflow
- SQLAlchemy videos
- Xpert Learning Assistant
