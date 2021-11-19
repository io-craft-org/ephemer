import logging
from urllib.request import urljoin

import requests

from .exceptions import OTreeAPIUsageError, OTreeNotAvailable
from .models import Participant, Session

logger = logging.getLogger(__name__)


class OTreeConnector:
    """Connector to talk to OTree5 through its REST API"""

    def __init__(self, api_uri):
        self.api_uri = api_uri

    def _get(self, endpoint, json_data={}, json_response=True):
        return self._call(requests.get, endpoint, json_data, json_response)

    def _post(self, endpoint, json_data={}, json_response=True):
        return self._call(requests.post, endpoint, json_data, json_response)

    def _call(self, caller, endpoint, json_data={}, json_response=True):
        url = self.api_uri + "/" + endpoint

        try:
            logger.info(f"{caller.__name__.upper()} {url}")
            resp = caller(url, json=json_data)
        except Exception as error:
            # XXX Maybe we could report what happened
            logger.error(error)
            raise OTreeNotAvailable(error)

        if resp.status_code == 400:
            logger.error(
                f"""
                HTTP 400 Client Error
                endpoint: {endpoint}
                data: {json_data}
                error message: {resp.content}
            """
            )

        if 400 <= resp.status_code < 500:
            raise OTreeAPIUsageError()
        elif resp.status_code >= 500:
            raise OTreeNotAvailable()

        if json_response:
            return resp.json()
        else:
            return resp

    def create_session(self, app_name):
        """Create a new session"""
        # XXX Handle session configuration
        data = self._post(
            "sessions",
            {
                "session_config_name": f"{app_name}",
                "num_participants": 5,
            },
        )

        return Session(
            handler=data["code"], join_in_code=data["session_wide_url"].split("/")[-1]
        )

    def get_session(self, session_id):
        """Return details of a session"""
        data = self._get(f"sessions/{session_id}")

        return Session(
            handler=session_id,
            join_in_code="/".split(data["session_wide_url"])[-1],
            num_participants=data["num_participants"],
            participants=[
                Participant.from_otree(p_data) for p_data in data["participants"]
            ],
        )

    def get_session_participants(self, session_id):
        """Return current participant details of a session"""
        data = self._get(f"sessions/{session_id}/participants")

        return [Participant.from_otree(p_data) for p_data in data]

    def session_advance_participant(self, participant_code):
        """Advance a given participant"""
        return self._post(f"participants/{participant_code}/advance")

    def get_session_results_as_csv(self, session_id):
        """Return the CSV results of a session"""
        return self._get(f"sessions/{session_id}/export", json_response=False)
