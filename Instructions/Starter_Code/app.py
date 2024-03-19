# Import the dependencies.
import os
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
db_path = '/Users/maia/Desktop/NU-VIRT-DATA-PT-10-2023-U-LOLC/02-Homework/10-Advanced-SQL/Instructions/Starter_Code/Resources/hawaii.sqlite'
if os.path.exists(db_path):
    engine = create_engine("sqlite:///" + db_path)
else:
    raise FileNotFoundError("SQLite file does not exist.")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
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

# Home page with all available API routes
@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation | Returns jsonified precipitation (in) data for the last year<br/>"
        f"/api/v1.0/stations | Returns jsonified list of stations<br/>"
        f"/api/v1.0/tobs | Returns jsonified temp (F) data for the last year<br/>"
        f"/api/v1.0/<start> | Returns min, max, and avg temp (F) after the given start date. Format: yyyy-mm-dd<br/>"
        f"/api/v1.0/<start>/<end> | Returns min, max, and avg temp (F) for the given date range. Format: yyyy-mm-dd/yyyy-mm-dd"
    )

# Page with precipitation data
@app.route("/api/v1.0/precipitation")
def prcpdata():
    """Return a list of all precipitation data for the last year"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).\
                      filter(Measurement.date >= dt.date(2016, 8, 23)).\
                      order_by(Measurement.date).all()
    session.close()

    prcp_data = [{"date": date, "precipitation": prcp} for date, prcp in results]
    return jsonify(prcp_data)

# Page with station data
@app.route("/api/v1.0/stations")
def stationinfo():
    """Return a list of all station data"""
    session = Session(engine)
    results = session.query(Station.station, Station.id).all()
    session.close()

    station_data = [{"station": station, "id": station_id} for station, station_id in results]
    return jsonify(station_data)

# Page with temperature data
@app.route("/api/v1.0/tobs")
def tobsdata():
    """Return a list of all temperature data for the last year"""
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
                           filter(Measurement.date >= dt.date(2016, 8, 23)).\
                           order_by(Measurement.date).all()
    session.close()

    tobs_data = [{"date": date, "temperature": tobs} for date, tobs in results]
    return jsonify(tobs_data)

# Page for finding temperature data after the given start date
@app.route("/api/v1.0/<start>")
def startinfo(start):
    """Return a list of the temperature statistics after the provided date"""
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                                filter(Measurement.date >= start).all()
    session.close()

    if temperature_stats:
        min_temp, max_temp, avg_temp = temperature_stats[0]
        return jsonify({"start_date": start, "min_temperature": min_temp, "max_temperature": max_temp, "avg_temperature": avg_temp})
    else:
        return jsonify({"error": "No temperature data found for the provided date."}), 404

# Page for finding temperature data between the given dates
@app.route("/api/v1.0/<start>/<end>")
def startendinfo(start, end):
    """Return a list of the temperature statistics between the provided dates"""
    session = Session(engine)
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                                filter(Measurement.date >= start).\
                                filter(Measurement.date <= end).all()
    session.close()

    if temperature_stats:
        min_temp, max_temp, avg_temp = temperature_stats[0]
        return jsonify({"start_date": start, "end_date": end, "min_temperature": min_temp, "max_temperature": max_temp, "avg_temperature": avg_temp})
    else:
        return jsonify({"error": "No temperature data found for the provided date range."}), 404

# Debugging
if __name__ == '__main__':
    app.run(debug=True)
