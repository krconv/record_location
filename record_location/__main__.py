import time

import schedule

from record_location import config, influx, life360, recorder


def main():
    schedule.every(config.Schedule.interval).minutes.do(_record)

    while True:
        schedule.run_pending()
        time.sleep(1)


def _record():
    location_api = life360.API()
    database_api = influx.API()

    recorder.Recorder(location_api, database_api).record()
