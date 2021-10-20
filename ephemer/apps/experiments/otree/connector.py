from urllib.request import urljoin

import requests

from .exceptions import OTreeNotAvailable
from .models import Participant, Session


class OTreeConnector:
    """Connector to talk to OTree5 through its REST API"""

    def __init__(self, api_uri):
        self.api_uri = api_uri

    def _get(self, endpoint, json_data={}):
        try:
            resp = requests.get(urljoin(self.api_uri, endpoint), json=json_data)
        except Exception:
            # XXX Maybe we could report what happened
            raise OTreeNotAvailable()

        return resp.json()

    def _post(self, endpoint, json_data={}):
        try:
            resp = requests.post(urljoin(self.api_uri, endpoint), json=json_data)
        except Exception:
            # XXX Maybe we could report what happened
            raise OTreeNotAvailable()

        return resp.json()

    def create_session(self, app_name):
        """Create a new session"""
        # XXX Handle session configuration
        data = self._post(
            "sessions",
            {
                "session_config_name": f"{app_name}",
                "num_participants": 1,
            },
        )

        return Session(handler=data["code"], participant_link=data["session_wide_url"])

    def get_session(self, session_id):
        """Return details of a session"""
        data = self._get(f"sessions/{session_id}")

        return Session(
            handler=session_id,
            participant_link=data["session_wide_url"],
            num_participants=data["num_participants"],
            participants=[
                Participant.from_otree(p_data) for p_data in data["participants"]
            ],
        )
