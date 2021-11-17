from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Participant:
    access_code: str
    id_in_session: int
    last_page_timestamp: int = None
    is_active: int = None
    current_page_name: str = None
    current_page_number: int = None
    total_page_count: int = None
    is_finished: bool = False

    @classmethod
    def from_otree(cls, data):
        timestamp = data.get("_last_page_timestamp", None)
        is_active = False
        if timestamp:
            now = datetime.now()
            elapsed = now - datetime.fromtimestamp(timestamp)
            is_active = elapsed < timedelta(minutes=5)

        current_page_number, total_page_count = data.get("_current_page", "0/0").split(
            "/"
        )

        return Participant(
            id_in_session=data["id_in_session"],
            access_code=data["code"],
            current_page_name=data.get("_current_page_name", None),
            last_page_timestamp=data.get("_last_page_timestamp", None),
            is_active=is_active,
            current_page_number=int(current_page_number),
            total_page_count=int(total_page_count),
            is_finished=(current_page_number == total_page_count),
        )


@dataclass
class Session:
    handler: str
    join_in_code: str
    participants: List[Participant] = field(default_factory=list)
    num_participants: int = 0
