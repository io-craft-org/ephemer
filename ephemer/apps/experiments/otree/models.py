from dataclasses import dataclass, field


@dataclass
class Participant:
    access_code: str
    id_in_session: int

    @classmethod
    def from_otree(cls, data):
        return Participant(
            id_in_session=data["id_in_session"], access_code=data["code"]
        )


@dataclass
class Session:
    handler: str
    participant_link: str
    participants: list[Participant] = field(default_factory=list)
    num_participants: int = 0
