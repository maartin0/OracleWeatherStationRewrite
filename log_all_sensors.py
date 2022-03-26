#!/usr/bin/python3
import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
from database import Database

import time

HEADERS = [
    "timestamp",
    "temperature0_c",
    "temperature1_c",
    "air_quality_percent",
    "pressure_mb",
    "humidity_percent",
    "wind_direction_degrees",
    "wind_speed_kmph",
    "wind_gust_kmph",
    "rainfall_mm",
]

if __name__ == "__main__":
    print("Reading...")
    pressure = bmp085.BMP085()
    temp_probe = ds18b20_therm.DS18B20()
    air_qual = tgs2600.TGS2600(adc_channel = 0)
    humidity = HTU21D.HTU21D()
    wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
    interrupts = interrupt_client.interrupt_client(port = 49501)

    wind_average = wind_dir.get_value(10) # ten seconds

    db = Database(HEADERS)

    print("Saving...")
    db.insert(
        time.time(),
        temp_probe.read_temp(),
        humidity.read_temperature(),
        air_qual.get_value(),
        pressure.get_pressure(),
        humidity.read_humidity(),
        wind_average,
        interrupts.get_wind(),
        interrupts.get_wind_gust(),
        interrupts.get_rain()
        )
    print("done")

    interrupts.reset()
