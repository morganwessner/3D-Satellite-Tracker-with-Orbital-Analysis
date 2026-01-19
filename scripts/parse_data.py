#parse 2LE data from file
import json
from pathlib import Path
from pyorbital.orbital import Orbital

#define paths
input_file = Path("data/tle/tle_data.txt")
output_dir = Path("data/tle_parsed")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "tle_data_parsed.json"

#load JSON data
with open(input_file, "r") as file:
    tle_json = json.load(file)
    
satellite_data = []

#start parsing TLE data
for satellite in tle_json:
    try:
        name = satellite.get("OBJECT_NAME", "Unknown")
        line1 = satellite.get("TLE_LINE1", "")
        line2 = satellite.get("TLE_LINE2", "")
        
        #create Orbital object
        orbital = Orbital(name, line1=line1, line2=line2)
        
        satellite_data.append({
            "name": name,
            "line1": line1,
            "line2": line2,
            "norad_id": satellite.get("NORAD_CAT_ID", None)
        })
    except Exception as e:
        print(f"Error parsing satellite {name}: {e}")
        
#save parsed data to local file
with open(output_file, "w") as file:
    json.dump(satellite_data, file, indent=4)
    
print("TLE data successfully parsed and saved.")