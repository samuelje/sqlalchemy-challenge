import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stats from start date (yyyy-mm-dd): /api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"Temperature stats from start to end dates (yyyy-mm-dd): /api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

# App route for precipitation data

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= "2016-08-23").\
        all()

    session.close()

#   Create dictionary for precipitation data
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)

# App route for station data

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).\
                order_by(Station.station).all()
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

# App route for one year data

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station == 'USC00519281').\
                order_by(Measurement.date).all()
    session.close()

#   Create dictionary for one year of prcp data
    all_tobs = []
    for prcp, date, tobs in results:
        tobs_dict = {}
        tobs_dict["prcp"] = prcp
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

# App route for data from start date
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()
    
    session.close()

#   Create dictionary start_date data
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict)
    return jsonify(start_date_tobs)

# App route for start to end date data
@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    session.close()
  
#   Create a dictionary for start to end date data
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)