import logging
from urllib.request import urljoin

import requests

from .exceptions import OTreeNotAvailable, OTreeAPIUsageError
from .models import Participant, Session


logger = logging.getLogger(__name__)


class OTreeConnector:
    """Connector to talk to OTree5 through its REST API"""

    def __init__(self, api_uri):
        self.api_uri = api_uri

    def _get(self, endpoint, json_data={}):
        return self._call(requests.get, endpoint, json_data)

    def _post(self, endpoint, json_data={}):
        return self._call(requests.post, endpoint, json_data)

    def _call(self, caller, endpoint, json_data={}):
        url = urljoin(self.api_uri, endpoint)
        try:
            logger.info(f"{caller.__name__.upper()} {url}")
            resp = caller(url, json=json_data)
        except Exception:
            # XXX Maybe we could report what happened
            raise OTreeNotAvailable()

        if resp.status_code == 400:
            logger.error(f'''
                HTTP 400 Client Error
                endpoint: {endpoint}
                data: {json_data}
                error message: {resp.content}
            ''')

        if 400 <= resp.status_code < 500:
            raise OTreeAPIUsageError()
        elif resp.status_code >= 500:
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
