from record_location import influx, life360, recorder


def main():
    location_api = life360.API()
    database_api = influx.API()

    recorder.Recorder(location_api, database_api).record()
