# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///......sqlite", echo = False)

# reflect an existing database into a new model and check keys
Base = automap_base()
Base.prepare(engine, reflect=True)
#Base.classes.keys()

# Save reference to the table
Table_nameee = Base.classes.table_nameee

# Flask Setup
app = Flask(__name__)


# Flask Routes
# Home Page
@app.route("/")
def home_page():
    """List all routes that are available."""
    return(f"Avaliable Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"............."
    )

# Json representation of dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all 
    results = session.query().all()

    session.close()
    return jsonify()

#Convert the query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.



# Station list
@app.route("/api/v1.0/stations")
def stations():

    # Return a JSON list of stations from the dataset.
    session.close()
    return()


# Temperature observations
@app.route("/api/v1.0/tobs")
def tobs():


#Query the dates and temperature observations of the most active station for 
#       the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.



# Temperature of certain dates
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end):


# Return a JSON list of the minimum temperature, the average temperature, and \
#       the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and 
#       TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
#       for dates between the start and end date inclusive.





#  Create way to run
if __name__ == '__main__':
    app.run(debug=True)