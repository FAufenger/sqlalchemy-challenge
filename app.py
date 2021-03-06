# Import dependencies
import numpy as np
import datetime as dt

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
        <html lang="en-us">
        <head>
            <meta charset="UTF-8">

        <style> 
            h1 {
                font-size: 35px;
                color: "white";
                background-color: "blue";
            }
            
            h2 {
                font-size: 20px;
                font-weight: bold;
            }
            
            </style>
            </head>

            <h1>Hawaii Climate App (Flask API)</h1>

            <h2>Precipitation:</h2>
            <p>JSON representation of dictionary (date: prcp)</p>
                <ul>
                    <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
                </ul>
            <h2>Stations:</h2>
            <p>JSON list of stations from the dataset</p>
                <ul>
                    <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
                </ul>

            <h2>Temperature:</h2>
            <p>A JSON list of temperature observations (TOBS)<br> 
                    for the last year recorded from the most active station</p>
                <ul>
                    <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
                </ul>
        
            <h2>Range of Temperature:</h2>
            <p>JSON list of the min temp, avg temp, and the max <br>
                temp for a given start or start-end range over all stations.</p>
                <ul>
                    <li><a href="/api/v1.0/date_search">/api/v1.0/date_search</a></li>
                </ul>
        </html> 
        """

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


# Temperature observations
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    # Query Data to find last date recorded and track back one year
    sel = [Measurement.date]
    last_date_str = session.query(*sel).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date_str[0], '%Y-%m-%d')
    year_ago = last_date - dt.timedelta(365)

    # Query Data to get station with most observations
    sel = [Measurement.station, func.count(Measurement.id)]
    active_stations = session.query(*sel).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).all()
    most_active_station = active_stations[0][0]
    
    # Use obtained dates and station to get results
    sel = Measurement.date, Measurement.tobs
    tobs_data = session.query(*sel).\
                filter(Measurement.date >= year_ago).\
                filter(Measurement.date <= last_date).\
                filter(Measurement.station == most_active_station).\
                order_by(Measurement.date).all()
    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_list = list(np.ravel(tobs_data))
    return jsonify(tobs_list)


@app.route("/api/v1.0/date_search")
def page_within_page():
    session = Session(engine)

    sel = [Measurement.date]
    recent_date_str = session.query(*sel).order_by(Measurement.date.desc()).first()
    recent_date = dt.datetime.strptime(recent_date_str[0], '%Y-%m-%d')
    
    oldest_record_str = session.query(*sel).order_by(Measurement.date.asc()).first()
    oldest_record = dt.datetime.strptime(oldest_record_str[0], '%Y-%m-%d')
    
    session.close()

    return(
        f"Hello!!"
        f"<br/>"
        f"<br/>"
        f"<br/>"
        f"The most recent date stored to this file is {recent_date}<br/>"
        f"While the oldest date on record is {oldest_record}<br/>"
        f"<br/>"
        f"<br/>"
        f"Please delete (date_search) from the http above and type in start date<br/> "
        f"type a YYYY-MM-DD to begin<br/>"
        f"<br/>"
        f"This starts a search from the chosen date to the most recent observation recorded<br/>"
        f"<br/>"
        f"<br/>"
        f"You also have the option to choose an end date to enclose the search range<br/>"
        f"You must add a forward slash between start/end can also be explained as<br/>" 
        f"YYYY-MM-DD/YYYY-MM-DD with start alwasy coming frist and if second variable <br/>"
        f"(end) is left empty or typed in incorrectly or not registering<br/>"
        f"end will default to last recorded observation<br/>"
        f"<br/>"
        f"<br/>"
        f"<br/>"
        f"Presented in Json for a list of chosen dates.<br/>"
        f"TMIN<br/>"
        f"TAVG<br/>"
        f"TMAX<br/>"
    )

# Temperature of certain dates (Combinng two possible queries from one def())
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

# Return a JSON list of the minimum temperature, the average temperature, and \
#       the max temperature for a given start or start-end range.
def temp_range(start, end = None):
    session = Session(engine)

    # Query Data to find last date recorded and track back one year
    sel = [Measurement.date]
    last_date_str = session.query(*sel).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date_str[0], '%Y-%m-%d')
    start_date = start
    end_date = end

    ## Attempt to make input easier into hyperlink....
    # Find desired start and end search date
    # start_date = input("YYYY-MM-DD")
    # end_date = input("YYYY-MM-DD")
    # print(f'Which date would you like to end:')
    # print(f'{start_date}')
    # print(f'Which date would you like to end:')
    # print(f'If left blank will default to most recent observation {last_date}')
    # print(f'{end_date}')

# When given the start only, calculate TMIN, TAVG, and 
#       TMAX for all dates greater than and equal to the start date.
    if end == None:
        sel = func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)
        temp_stats = session.query(*sel).\
            filter(Measurement.date.between(start_date, last_date)).all()
        
        temp_stats_list = list(np.ravel(temp_stats))
        return jsonify(temp_stats_list)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
#       for dates between the start and end date inclusive.
    else:
        sel = func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)
        temp_stats = session.query(*sel).\
            filter(start_date < end_date).all()
       
        temp_stats_list = list(np.ravel(temp_stats))
        return jsonify(temp_stats_list)


    session.close()

#  Create way to run
if __name__ == '__main__':
    app.run(debug=True)