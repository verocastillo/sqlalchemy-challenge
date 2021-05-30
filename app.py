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
from sqlalchemy.sql.expression import null

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
    precdicts = {"Measurements" : precdict}
    # Return JSON of dictionary
    return jsonify(precdicts)

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
    statdict = {"Station Names" : statnames}
    # Return JSON of dictionary
    return jsonify(statdict)

    # Temperature Route
    # Query the dates and temperature observations of the most active station for the last year of data.
@app.route("/api/v1.0/tobs")
def temps():
    # Create session
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
    #  Calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    #Create session and start query
    session = Session(engine)
    stdate = dt.strptime(start, '%Y-%m-%d')
    datestats = session.query(measurements.date,func.avg(measurements.tobs),
                func.max(measurements.tobs),func.min(measurements.tobs)).\
                filter(measurements.date >= stdate.strftime('%Y-%m-%d')).\
                group_by(measurements.date).all()
    session.close()
    # Get measurements as dictionaries
    vals = []
    startdates = []
    for date in datestats:
        startdates.append(date[0])
        vals.append({'Average Temperature': round(int(date[1]),4),
        'Max Temperature': round(int(date[2]),4),
        'Min Temperature': round(int(date[3]),4)})
    startdict = dict.fromkeys(startdates,0)
    counter = 0
    for date in startdates:
        startdict[str(date)] = vals[counter]
        counter = counter + 1
    return jsonify(startdict)

    # Start/End Route
@app.route("/api/v1.0/<start>/<end>")
def stenroute(start,end):
    #Create session and start query
    session = Session(engine)
    stdate = dt.strptime(start, '%Y-%m-%d')
    nddate = dt.strptime(end, '%Y-%m-%d')
    # Run query
    datestats = session.query(measurements.date,func.avg(measurements.tobs),
                func.max(measurements.tobs),func.min(measurements.tobs)).\
                filter(measurements.date >= stdate.strftime('%Y-%m-%d')).\
                filter(measurements.date <= nddate.strftime('%Y-%m-%d')).\
                group_by(measurements.date).all()
    session.close()
    # Get measurements as dictionaries
    vals = []
    startdates = []
    for date in datestats:
        startdates.append(date[0])
        vals.append({'Average Temperature': round(int(date[1]),4),
        'Max Temperature': round(int(date[2]),4),
        'Min Temperature': round(int(date[3]),4)})
    # Error message if second date is before the first date
    if len(startdates) < 1:
        startdict = "Error! Choose two valid dates."
    # Build dictionary
    else:
        startdict = dict.fromkeys(startdates,0)
        counter = 0
        for date in startdates:
            startdict[str(date)] = vals[counter]
            counter = counter + 1
    return jsonify(startdict)

if __name__ == '__main__':
    app.run(debug=True)
