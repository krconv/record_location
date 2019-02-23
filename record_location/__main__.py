import sys
import time

from loguru import logger
import schedule

from record_location import config, influx, life360, recorder


@logger.catch
def main():
    _setup_logger()

    _setup_schedule()

    _loop()


def _setup_logger():
    logger.remove(0)
    logger.add(sys.stderr, level=config.Logging.level)


def _setup_schedule():
    interval = config.Schedule.interval
    logger.info(f"Will record location every {interval} minute(s)")

    schedule.every(interval).minutes.do(_record)


def _record():
    logger.debug("About to record...")

    location_api = life360.API()
    database_api = influx.API()

    recorder.Recorder(location_api, database_api).record()


def _loop():
    logger.debug("Looping on schedule forever")

    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)
