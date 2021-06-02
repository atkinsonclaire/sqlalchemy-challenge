from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precip_results = session.query(Precipitation.date, Precipitation.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in precip_results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations_results = session.query(Stations.stations).all()

    session.close()

    return jsonify(stations_results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    tobs_results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date < '2017-08-18').\
        filter(Measurement.date > '2016-08-18').\
        order_by(Measurement.date).all()

    session.close()

    return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def start(start_date):
    session=Session(engine)
    start_date_results=session.query(Measurement.date, Measurement.tobs)

    for start in start_date_results:
        TMIN=session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start)
        TMAX=session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start)
        TAVG=session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.station >= start)
    session.close()
        
    return jsonify({"Min Temp": {TMIN}, "Max Temp:": {TMAX}, "Avg Temp": {TAVG} })

@app.route("/api/v1.0/<start>/<end>")
def end(start_date, end_date):
    session=Session(engine)
    date_results=session.query(Measurement.date, Measurement.tobs)

    for start, end in date_results:
        TMIN=session.query(func.min(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end)
        TMAX=session.query(func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end)
        TAVG=session.query(func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end)
    session.close()
        
    return jsonify({"Min Temp": {TMIN}, "Max Temp:": {TMAX}, "Avg Temp": {TAVG} })


if __name__ == "__main__":
    app.run(debug=True)
