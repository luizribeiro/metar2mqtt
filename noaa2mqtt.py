import ftplib
import json
from io import BytesIO

from paho.mqtt import publish
from metar import Metar

FTP_SERVER = "tgftp.nws.noaa.gov"
FTP_PATH = "/data/observations/metar/stations/KEWR.TXT"

with ftplib.FTP(FTP_SERVER) as ftp:
    ftp.login()
    with BytesIO() as f:
        ftp.retrbinary(f"RETR {FTP_PATH}", f.write)
        f.seek(0)
        lines = f.read().decode().splitlines()[1:]
        metar_data = Metar.Metar("\n".join(lines))

payload = {
    "station": metar_data.station_id,
    "time": str(metar_data.time),
    "temperature": metar_data.temp.value("C"),
    "dewpoint": metar_data.dewpt.value("C"),
    "wind_direction": metar_data.wind_dir.value(),
    "wind_speed_mph": metar_data.wind_speed.value("MPH"),
    "visibility": metar_data.visibility(),
    "pressure_mbar": metar_data.press.value("MB"),
    "weather": metar_data.weather,
    "precipitation_1h": metar_data.precip_1hr,
    "precipitation_3h": metar_data.precip_3hr,
    "precipitation_6h": metar_data.precip_6hr,
}

print(payload)

#publish.single("metar", json.dumps(payload), hostname="mqtt.example.com")
