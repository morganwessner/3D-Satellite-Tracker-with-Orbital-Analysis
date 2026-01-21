import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from pyorbital.orbital import Orbital

class SatellitePropagator:
    def __init__(self, tle_data):
        self.orbitals = {}
        self.load_tle_data(tle_data)
        
    def load_tle_data(self, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"TLE data file not found: {path}")
        
        with open(path, "r") as file:
            satellites = json.load(file)
            
        for satellite in satellites:
            self.orbitals[satellite["norad_id"]] = Orbital(
                satellite["name"],
                line1=satellite["line1"],
                line2=satellite["line2"]
            )
            
    def propagate(self, norad_id, time):
        orbital = self.orbitals[norad_id]
        position, velocity = orbital.get_position(time, normalize=False)
        return position, velocity
    
    def propagate_all(self, time):
        results = {}
        for norad_id, orbital in self.orbitals.items():
            position, velocity = orbital.get_position(time, normalize=False)
            results[norad_id] = {
                "position": position,
                "velocity": velocity
            }
        return results
    
    def propagate_over_time(self, norad_id, start_time, duration_minutes, step_seconds):
        results = []
        orbital = self.orbitals[norad_id]
        
        current = start_time
        end = start_time + timedelta(minutes=duration_minutes)
        
        while current <= end:
            position, velocity = orbital.get_position(current, noramlize=False)
            results.append({
                "time": current,
                "position": position,
                "velocity": velocity
            })
            current += timedelta(seconds=step_seconds)
        return results