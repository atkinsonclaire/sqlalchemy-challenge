from flask import flask, jsonify
app=Flask(_name_)

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

    results = session.query(Precipitation.date, Precipitation.prcp).all()

    session.close()

    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations)
def stations():
    session = Session(engine)

    results = session.query(Stations.stations).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs)
def tobs():
    session = Session(engine)

    results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date < '2017-08-18').\
        filter(Measurement.date > '2016-08-18').\
        order_by(Measurement.date).all()

    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>)
def start():
    session = Session(engine)

    min_temp=session.query(func.min(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281')
    max_temp=session.query(func.max(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281')
    avg_temp=session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281')
    session.close()

    all_min = list(np.ravel(min_temp))
    return jsonify(all_min)
    all_max = list(np.ravel(max_temp))
    return jsonify(all_max)
    all_avg = list(np.ravel(avg_temp))
    return jsonify(all_avg)

if __name__ == '__main__':
    app.run(debug=True)
