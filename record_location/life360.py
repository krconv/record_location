import datetime

import attr
from loguru import logger
import requests

from record_location import config


@attr.s
class API:
    base_url = attr.ib(default=config.Life360.base_url)
    auth = attr.ib(default=config.Life360.auth)

    def get_circles(self):
        logger.debug("Requesting all circles from Life360")
        response = self._request("circles/")
        circles = []
        for circle_data in response["circles"]:
            circle = _Circle.from_dict(circle_data)
            circles.append(circle)
        return circles

    def get_members(self, circle):
        logger.debug(f"Requesting all members for circle '{circle.name}' from Life360")
        response = self._request(f"circles/{circle.id}/members")
        members = []
        for member_data in response["members"]:
            member = _Member.from_dict(member_data)
            members.append(member)
        return members

    def get_location(self, circle, member):
        logger.debug(
            f"Requesting the location for member '{member.first_name}' from Life360"
        )
        response = self._request(f"circles/{circle.id}/members/{member.id}/")
        location = _Location.from_dict(response["location"])
        return location

    def _request(self, endpoint):
        headers = {"Authorization": self.auth, "Accept": "application/json"}
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers)
        logger.debug(f"Got response with code '{response.status_code}' from Life360")
        return response.json()


@attr.s
class _Circle:
    id = attr.ib(type=str)
    name = attr.ib(type=str)

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], name=data["name"])


@attr.s
class _Member:
    id = attr.ib(type=str)
    first_name = attr.ib(type=str)

    @classmethod
    def from_dict(cls, data):
        return cls(id=data["id"], first_name=data["firstName"])


@attr.s
class _Location:
    timestamp = attr.ib(type=datetime.datetime)

    latitude = attr.ib(type=float)
    longitude = attr.ib(type=float)
    accuracy = attr.ib(type=int)

    place = attr.ib(type=str)

    battery_level = attr.ib(type=float)
    is_charging = attr.ib(type=bool)

    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=datetime.datetime.fromtimestamp(int(data["timestamp"])),
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"]),
            accuracy=int(data["accuracy"]),
            place=data["name"],
            battery_level=float(data["battery"]) / 100,
            is_charging=int(data["charge"]) == 1,
        )
