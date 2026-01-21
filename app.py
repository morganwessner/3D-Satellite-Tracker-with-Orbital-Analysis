#script for visualization and backend (FastAPI)
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from datetime import datetime, timezone
from scripts.propagate_tle import SatellitePropagator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#initialize the satellite propagator with TLE data
propagator = SatellitePropagator("scripts/data/tle_parsed/tle_data_parsed.json")

#load environment variables
load_dotenv()

#read token from environment
CESIUM_TOKEN = os.getenv("CESIUM_TOKEN")

@app.get("/cesium-token")
def get_token():
    return {"token": CESIUM_TOKEN}

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
    if norad_id not in propagator.orbitals:
        return {"error": "Satellite with given ID not found"}
    now = datetime.now(timezone.utc)
    position, velocity = propagator.propagate(norad_id, now)
    
    position = [float(x) for x in position]
    velocity = [float(x) for x in velocity]
    
    return {
        "norad_id": norad_id,
        "time": now.isoformat(),
        "position": position,
        "velocity": velocity
    }
    
#enpoint to get trajectory over time for a satellite
@app.get("/trajectory/{norad_id}")
def trajectory(norad_id: str, duration_minutes: int = 60, step_seconds: int = 10):
    start_time = datetime.now(timezone.utc)
    trajectory_data = propagator.propagate_over_time(norad_id, start_time, duration_minutes, step_seconds)
    
    #convert positions and velocities to floats for JSON
    for point in trajectory_data:
        point["position"] = [float(x) for x in point["position"]]
        point["velocity"] = [float(x) for x in point["velocity"]]
        point["time"] = point["time"].isoformat()
    return trajectory_data