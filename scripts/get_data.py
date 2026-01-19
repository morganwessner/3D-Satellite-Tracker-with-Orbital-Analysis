#gets data from Space-Track API and saves it locally 
from dotenv import load_dotenv
import os
import requests
from pathlib import Path

#load environment from .env file
load_dotenv()

#get environment variables for Space-Track credentials
USERNAME = os.getenv("SPACETRACK_USER")
PASSWORD = os.getenv("SPACETRACK_PASS")

#check is credentials are set
if not USERNAME or not PASSWORD:
    raise RuntimeError("Space-Track credentials not set in environment variables.")

#create session
session = requests.Session()

#login to Space-Track
LOGIN_URL = "https://www.space-track.org/ajaxauth/login"

response = session.post(LOGIN_URL, data={"identity": USERNAME, "password": PASSWORD})

#verify login was successful
if response.status_code != 200 or "Invalid" in response.text:
    raise RuntimeError("Failed to log in to Space-Track. Check your credentials.")

#define TLE data query URL (first 50 objects updated in the last 30 days)
TLE_QUERY_URL = (
    "https://www.space-track.org/basicspacedata/query/"
    "class/gp/EPOCH/%3Enow-30/"
    "ORDERBY/NORAD_CAT_ID,EPOCH/"
    "LIMIT/50/format/2le"
)

#get all the TLE data
response = session.get(TLE_QUERY_URL)
tle_text = response.text.strip()


#check that directory exists
output_dir = Path("data/tle")
output_dir.mkdir(parents=True, exist_ok=True)
file_path = output_dir / "tle_data.txt"

#save TLE data to local file
with open(file_path, "w") as file:
    file.write(tle_text)

print("Satellite data successfully retrieved and saved.")