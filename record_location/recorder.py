import attr

from record_location import config, influx


@attr.s
class Recorder:
    location_api = attr.ib()
    database_api = attr.ib()
    fields = attr.ib(default=config.Recorder.fields)

    def record(self):
        points = self._gather_points()

        self._write_points(points)

    def _gather_points(self):
        points = []
        for circle in self.location_api.get_circles():
            for member in self.location_api.get_members(circle):
                location = self.location_api.get_location(circle, member)

                member_points = self._gather_points_from_member(member, location)
                points += member_points
        return points

    def _gather_points_from_member(self, member, location):
        points = []
        for field in self.fields:
            point = self._create_point(member, location, field)
            points.append(point)
        return points

    def _create_point(self, member, location, field):
        return influx.Point(
            measurement=field["name"],
            tags={"person": member.first_name.lower()},
            fields={"value": getattr(location, field["attribute"])},
            timestamp=location.timestamp,
        )

    def _write_points(self, points):
        self.database_api.write_points(points)
