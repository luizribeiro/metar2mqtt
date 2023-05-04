import ftplib
import json
from datetime import datetime
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

def value(x, unit):
    return x.value(unit) if x else None

payload = {
    "timestamp": int(datetime.timestamp(metar_data.time)),
    "station": metar_data.station_id,
    "cycle": metar_data.cycle,
    "dewpoint": value(metar_data.dewpt, "C"),
    "ice_accretion_in_1h": value(metar_data.ice_accretion_1hr, "IN"),
    "ice_accretion_in_3h": value(metar_data.ice_accretion_3hr, "IN"),
    "ice_accretion_in_6h": value(metar_data.ice_accretion_6hr, "IN"),
    "max_temperature_24h": value(metar_data.max_temp_24hr, "C"),
    "max_temperature_6h": value(metar_data.max_temp_6hr, "C"),
    "min_temperature_24h": value(metar_data.min_temp_24hr, "C"),
    "min_temperature_6h": value(metar_data.min_temp_6hr, "C"),
    "precipitation_in_1h": value(metar_data.precip_1hr, "IN"),
    "precipitation_in_24h": value(metar_data.precip_24hr, "IN"),
    "precipitation_in_3h": value(metar_data.precip_3hr, "IN"),
    "precipitation_in_6h": value(metar_data.precip_6hr, "IN"),
    "present_weather": metar_data.present_weather() if metar_data.weather else None,
    "pressure_mbar": value(metar_data.press, "MB"),
    "pressure_sea_level_mb": value(metar_data.press_sea_level, "MB"),
    "snow_depth_in": value(metar_data.snowdepth, "IN"),
    "temperature": value(metar_data.temp, "C"),
    "visibility_mi": value(metar_data.vis, "SM"),
    "wind_direction": metar_data.wind_dir.value(),
    "wind_gust_speed_mph": value(metar_data.wind_gust, "MPH"),
    "wind_speed_mph": value(metar_data.wind_speed, "MPH"),
    "wind_speed_peak_mph": value(metar_data.wind_speed_peak, "MPH"),
}

publish.single(f"metar/observation/{metar_data.station_id}", json.dumps(payload), hostname="sodium")
