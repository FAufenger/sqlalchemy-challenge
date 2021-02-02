# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo = False)

# reflect an existing database into a new model and check keys
Base = automap_base()
Base.prepare(engine, reflect=True)
#Base.classes.keys()

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)


# Flask Routes
# Home Page
@app.route("/")
def home_page():
    """List all routes that are available."""
    return"""
        <html>
            <h1>Hawaii Climate App (Flask API)</h1>
                    
            <p>Precipitation: JSON representation of dictionary</p>
                <ul>
                    <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
                </ul>
            <p>Stations: JSON list of stations from the dataset.</p>
                <ul>
                    <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
                </ul>
            <p>Temperature: Analysis of last recorded year</p>
                <ul>
                    <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
                </ul>
        </html> 
        """
# <img src="https://i.ytimg.com/vi/3ZiMvhIO-d4/maxresdefault.jpg" alt="Hawaii Weather"/>

# Json representation of dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    sel = [Measurement.date, Measurement.prcp]

    # Query all 
    prcp_result  = session.query(*sel).all()
    session.close()

    # Create a dictionary from the row data and append to a list of prcp
    prcp_list = []
    for date, prcp in prcp_result:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


# Station list
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel =  [Station.station]
    stations_list = session.query(*sel).all()
    session.close()

    # Convert list of tuples into normal list
    station_data = list(np.ravel(stations_list))
    
    # Return a JSON list of stations from the dataset.
    return jsonify(station_data)


# # Temperature observations
# @app.route("/api/v1.0/tobs")
# def tobs():


#Query the dates and temperature observations of the most active station for 
#    the last year of data.

#Return a JSON list of temperature observations (TOBS) for the previous year.



# # Temperature of certain dates
# @app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")

# def temp_range(start, end = None):


# # Return a JSON list of the minimum temperature, the average temperature, and \
# #       the max temperature for a given start or start-end range.
# # When given the start only, calculate TMIN, TAVG, and 
# #       TMAX for all dates greater than and equal to the start date.
# # When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
# #       for dates between the start and end date inclusive.





#  Create way to run
if __name__ == '__main__':
    app.run(debug=True)