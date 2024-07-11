# Import the dependencies.
from Flask import Flask, jsonify
from Flask_sqlalchemy import SQLAlchemy
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

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# reflect the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=db.engine)

#################################################
# Flask Setup
#################################################

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
