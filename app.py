import sqlalchemy
from flask import Flask
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)
S=Base.classes.station
M=Base.classes.measurement

session=Session(engine)

app = Flask(__name__)

@app.route('/')
def hoempage():
    return '''
        <h1>Hawaii's App</h1>
        <h2>The following routes are available:</h2>
        <ul>
            <li>/api/v1.0/precipitation</li>
            <li>/api/v1.0/stations</li>
            <li>/api/v1.0/tobs</li>
            <li>/api/v1.0/[start-date]</li>
            <li>/api/v1.0/[start-date]/[end-date]</li>
        </ul>
        '''

@app.route('/api/v1.0/precipitation')
def precipitation():

    results = session.query(M.date,M.prcp).filter(M.date>='2016-08-23').all()
    return { d:p for d,p in results }

@app.route('/api/v1.0/stations')
def stations():

    results = session.query(S.station,S.name).all()
    return { id:loc for id,loc in results }

@app.route('/api/v1.0/tobs')
def tobs():

    results = session.query(M.date, M.tobs ).filter(M.date>='2016-08-23').all()
    return { id:loc for id,loc in results }

@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dateRange(start, end='2017-08-23'):

    results = session.query(M.date, M.tobs).filter((M.date>=start)&(M.date<=end)).all()
    return { id:loc for id,loc in results }

    return f'''
        This is the start date: {start} <br>
        This is the end date: {end}
    '''



