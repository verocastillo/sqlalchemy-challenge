# Climate App
#
# 1. Import Flask
from flask import Flask, jsonify

# 2. Import Dependencies
import numpy as np
from datetime import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.inspection import inspect

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
