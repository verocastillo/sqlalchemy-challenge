# Climate App
#
# 1. Import Dependencies
import numpy as np
from datetime import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 2. Import Flask
from flask import Flask, jsonify

# 3. Setup Database
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to each table
measurements = Base.classes.measurement
stations = Base.classes.station

# 4. Setup Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# 5. Define Routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate API!<br/>"
        f"The following routes are available:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# 6. Define Query for Each Route

    # Precipitation Route
    # Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precip():
    # Create session and query
    session = Session(engine)
    resultss = session.query(measurements.date, measurements.prcp).all()
    session.close()
    # Get dictionary from results
    results = []
    for result in resultss:
        if result[1] != None :
            results.append(result)
    precdates = []
    for date in results:
        if date[0] not in precdates:
            precdates.append(date[0])
    precdict = dict.fromkeys(precdates,0)
    for prdate in precdates:
        precdict[str(prdate)] = []
        for date in results:
            if date[0] == prdate:
                precdict[str(prdate)].append(date[1])
    # Return JSON of dictionary
    return jsonify(precdict)

    # Stations Route
    # Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stats():
    # Create session and query
    session = Session(engine)
    results = session.query(measurements.station,stations.id,func.count(measurements.station)).\
        filter(measurements.station == stations.station).\
        group_by(measurements.station).all()
    session.close()
    # Get a list of the stations 
    statnames = []
    for result in results:
        statnames.append(result[0])
    # Return JSON of dictionary
    return jsonify(statnames)

    # Temperature Route
    # Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def temps():
    # Create session and query
    session = Session(engine)
    # Design a query to find the most active station
    actstation = session.query(measurements.station,stations.id,func.count(measurements.station)).\
        filter(measurements.station == stations.station).\
        group_by(measurements.station).order_by(func.count(measurements.station).desc()).first()
    actid = actstation[1]
    # Using the most active station id, get the most recent measurement
    recdate = session.query(measurements).\
        filter(measurements.station == stations.station).\
        filter(stations.id == int(actid)).\
        order_by(measurements.date.desc()).first()
    recdate = recdate.date
    # Starting from the most recent data point in the database. 
    date0 = dt.strptime(recdate, '%Y-%m-%d')
    # Calculate the date one year from the last date in
    yearago = date0.year - 1
    date1 = f'{yearago}-{date0.month}-{date0.day}'
    date1 = dt.strptime(date1, '%Y-%m-%d')
    # Obtain measurements for the last 12 months
    precactive_q = session.query(stations.id, measurements.station, measurements.date, measurements.tobs).\
        filter(measurements.station == stations.station).\
        filter(measurements.date > date1.strftime('%Y-%m-%d')).\
        filter(stations.id == int(actid)).\
        order_by(measurements.date).all()
    session.close()
    # Create dictionary with information
    tempdates = []
    temptemps = []
    for date in precactive_q:
        if date[2] not in tempdates:
            tempdates.append(date[2])
        temptemps.append(date[3])
    tempdict = dict.fromkeys(tempdates, 0)
    counter = 0
    for date in tempdates:
        tempdict[str(date)] = tempdict[str(date)] + temptemps[int(counter)]
        counter = counter + 1
    tempdics = {"Station ID" : precactive_q[0][0], "Station Name" : precactive_q[0][1], "Measurements" : tempdict}
    # Return JSON of dictionary
    return jsonify(tempdics)

    # Start Route
@app.route("/api/v1.0/<start>")
def stroute(start):
    return

    # Start/End Route
@app.route("/api/v1.0/<start>/<end>")
def stenroute(start,end):
    return

if __name__ == '__main__':
    app.run(debug=True)
