#script for visualization and backend (FastAPI)
from fastapi import FastAPI
from datetime import datetime, timezone
from scripts.propagate_tle import SatellitePropagator

app = FastAPI()

#initialize the satellite propagator with TLE data
propagator = SatellitePropagator("scripts/data/tle_parsed/tle_data_parsed.json")

#root endpoint to check API status
@app.get("/")
def root():
    return {"status": "Satellite Tracker API is running"}

#endpoint to get unique id of all satellites
@app.get("/satellites")
def list_satellites():
    return list(propagator.orbitals.keys())

#endpoint to get current state (position and velocity) of satellite (contains bug)
@app.get("/state/{norad_id}")
def satellite_state(norad_id: str):
    now = datetime.now(timezone.utc)
    position, velocity = propagator.propagate(norad_id, now)
    
    return {
        "norad_id": norad_id,
        "time": now.isoformat(),
        "position": position,
        "velocity": velocity
    }