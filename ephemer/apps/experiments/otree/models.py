from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Participant:
    access_code: str
    id_in_session: int
    last_page_timestamp: int = None
    current_page_name: str = None

    @classmethod
    def from_otree(cls, data):
        return Participant(
            id_in_session=data["id_in_session"],
            access_code=data["code"],
            current_page_name=data.get("_current_page_name", None),
            last_page_timestamp=data.get("_last_page_timestamp", None),
        )


@dataclass
class Session:
    handler: str
    join_in_code: str
    participants: List[Participant] = field(default_factory=list)
    num_participants: int = 0
