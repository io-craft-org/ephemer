import logging
import re
from urllib.parse import urlparse

import requests

from .exceptions import OTreeAPIUsageError, OTreeNotAvailable
from .models import Participant, Session

logger = logging.getLogger(__name__)


class OTreeConnector:
    """Connector to talk to OTree5 through its REST API"""

    def __init__(self, api_uri, api_key):
        self.api_uri = api_uri
        self.api_key = api_key

    def _get(self, endpoint, json_data={}, json_response=True):
        return self._call(requests.get, endpoint, json_data, json_response)

    def _post(self, endpoint, json_data={}, json_response=True):
        return self._call(requests.post, endpoint, json_data, json_response)

    def _call(self, caller, endpoint, json_data={}, json_response=True):
        url = self.api_uri + "/" + endpoint
        headers = {}

        if self.api_key:
            headers["otree-rest-key"] = self.api_key

        try:
            logger.info(f"{caller.__name__.upper()} {url}")
            resp = caller(url, json=json_data, headers=headers)
        except Exception as error:
            logger.error(error)
            raise OTreeNotAvailable(error)

        if resp.status_code >= 400:
            msg = f"""
                    HTTP {resp.status_code} Client Error
                    endpoint: {endpoint}
                    data: {json_data}
                    error message: {resp.content}
                """
            logger.error(msg)
            if 400 <= resp.status_code < 500:
                raise OTreeAPIUsageError(msg)
            elif resp.status_code >= 500:
                raise OTreeNotAvailable(msg)

        if json_response:
            return resp.json()
        else:
            return resp

    def create_session(self, app_name, num_participants):
        """Create a new session"""
        data = self._post(
            "sessions",
            {
                "session_config_name": f"{app_name}",
                "num_participants": num_participants,
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
            participants=self._make_participants(data["participants"]),
        )

    def get_session_participants(self, session_id):
        """Return current participant details of a session"""
        data = self._get(f"sessions/{session_id}/participants")
        return self._make_participants(data)

    def session_advance_participant(self, participant_code):
        """Advance a given participant"""
        return self._post(f"participants/{participant_code}/advance")

    def get_session_results_for_app_as_csv(self, session_id, app_name):
        """Return the CSV results of a session"""
        return self._get(
            f"sessions/{session_id}/export/app/{app_name}", json_response=False
        )

    def _make_participants(self, data):
        participants = [Participant.from_otree(p_data) for p_data in data]
        participants.sort(key=lambda participant: participant.id_in_session)
        return participants


def get_next_participant_code(otree_host, session_wide_code):
    def handle_error(resp):
        if resp.status_code == 404 and resp.text == "Session is full.":
            return
        raise OTreeNotAvailable(
            f"""
            HTTP {resp.status_code} Client Error
            endpoint: {resp.url}
            error message: {resp.content}
        """
        )

    join_path = "/join/"
    response = requests.get(otree_host + join_path + session_wide_code)
    if response.status_code != 200:
        handle_error(response)
        return None
    match_result = re.match("^/p/([a-zA-Z0-9]+)/", urlparse(response.url).path)
    return match_result.groups()[0]
