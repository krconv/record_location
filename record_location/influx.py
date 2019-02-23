
import datetime

import attr
import influxdb

from record_location import config


class Error(Exception):
    pass


class InvalidMeasurementError(Error):
    pass


class InvalidFieldsError(Error):
    pass


@attr.s
class API:
    host = attr.ib(default=config.InfluxDB.host)
    port = attr.ib(default=config.InfluxDB.port)
    username = attr.ib(default=config.InfluxDB.username)
    password = attr.ib(default=config.InfluxDB.password)
    database = attr.ib(default=config.InfluxDB.database)

    _client = attr.ib(init=False)

    @_client.default
    def _create_client(self):
        return influxdb.InfluxDBClient(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
        )

    def write_point(self, point):
        self.write_points([point])

    def write_points(self, points):
        self._write({ "points": [ point.serialize() for point in points ] })

    def _write(self, data):
        self._client.write(data, params=self._params_for_write())

    def _params_for_write(self):
        return { "db" : self.database }


@attr.s
class Point:
    measurement = attr.ib(type=str)
    tags = attr.ib(type=dict)
    fields = attr.ib(type=dict)
    timestamp = attr.ib(type=datetime.datetime)

    def serialize(self):
        self._validate()

        serialized = {
            "measurement": self.measurement,
            "tags": self.tags,
            "fields": self.fields,
        }

        if self.timestamp:
            serialized["time"] = self.timestamp

        return serialized

    def _validate(self):
        self._validate_measurement()
        self._validate_tags()
        self._validate_fields()
        self._validate_timestamp()

    def _validate_measurement(self):
        if not self.measurement:
            raise InvalidMeasurementError()

    def _validate_tags(self):
        pass

    def _validate_fields(self):
        if not self.fields:
            raise InvalidFieldsError()

    def _validate_timestamp(self):
        pass
