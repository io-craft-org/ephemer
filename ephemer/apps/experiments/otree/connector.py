from urllib.request import urljoin

import requests

from .exceptions import OTreeNotAvailable
from .models import Session


class OTreeConnector:
    """Connector to talk to OTree5 through its REST API"""

    def __init__(self, api_uri):
        self.api_uri = api_uri

    def _call(self, endpoint, json_data):
        try:
            resp = requests.post(urljoin(self.api_uri, endpoint), json=json_data)
        except Exception:
            # XXX Maybe we could report what happened
            raise OTreeNotAvailable()

        return resp.json()

    def create_session(self):
        """Create a new session"""
        # XXX Handle session names and configuration
        data = self._call(
            "sessions",
            {
                "session_config_name": "survey",
                "num_participants": 3,
            },
        )

        return Session(handler=data["code"], participant_link=data["session_wide_url"])
