class Life360:
    base_url = "https://www.life360.com/v3/"
    auth = "Bearer super_secret_token"


class InfluxDB:
    host = "influx.example.com"
    port = 8086
    username = "username"
    password = "password"
    database = "database"


class Recorder:
    fields = [
        {"name": "location/latitude", "attribute": "latitude"},
        {"name": "location/longitude", "attribute": "longitude"},
        {"name": "location/accuracy", "attribute": "accuracy"},
        {"name": "location/place", "attribute": "place"},
        {"name": "battery_level", "attribute": "battery_level"},
        {"name": "is_charging", "attribute": "is_charging"},
    ]
