import requests

OTREE_HOST = "localhost"
OTREE_PORT = 8001


def create_session(experiment_name, num_participants):
    # response format:
    # {
    #     'admin_url': 'http://localhost:8001/SessionStartLinks/zz1usouu',
    #     'code': 'zz1usouu',
    #     'session_wide_url': 'http://localhost:8001/join/kehikome'
    # }
    resp = requests.post(
        f"http://{OTREE_HOST}:{OTREE_PORT}/api/sessions",
        json={
            "session_config_name": experiment_name,
            "num_participants": num_participants,
        },
    )
    return resp.json()


def get_session(code):
    # response format:
    # {
    #     'REAL_WORLD_CURRENCY_CODE': 'USD',
    #     'admin_url': 'http://localhost:8001/SessionStartLinks/93r6k4ov',
    #     'config': {'app_sequence': ['survey', 'payment_info'],
    #                'display_name': 'survey',
    #                'doc': '',
    #                'name': 'survey',
    #                'num_demo_participants': 1,
    #                'participation_fee': 0.0,
    #                'real_world_currency_per_point': 1.0},
    #     'num_participants': 3,
    #     'participants': [{'code': '3cro7uw4',
    #                       'id_in_session': 1,
    #                       'label': None,
    #                       'payoff_in_real_world_currency': 0.0},
    #                      {'code': 'rg77qgh9',
    #                       'id_in_session': 2,
    #                       'label': None,
    #                       'payoff_in_real_world_currency': 0.0},
    #                      {'code': 'a8wx034q',
    #                       'id_in_session': 3,
    #                       'label': None,
    #                       'payoff_in_real_world_currency': 0.0}],
    #     'session_wide_url': 'http://localhost:8001/join/juvutiru'
    # }
    resp = requests.get(
        f"http://{OTREE_HOST}:{OTREE_PORT}/api/sessions/{code}",
    )
    return resp.json()


def get_session_participants(code):
    # Response format:
    # [
    #     {
    #         "_current_app_name": "FGES_Louvain",
    #         "_current_page": "5/20",
    #         "_current_page_name": "Test4_Page",
    #         "_last_page_timestamp": 1634117391,
    #         "_monitor_note": null,
    #         "_numeric_label": "P1",
    #         "_round_number": 1,
    #         "code": "ud4myvih",
    #         "id_in_session": 1,
    #         "label": null
    #     },
    #     ...
    # ]
    resp = requests.get(
        f"http://{OTREE_HOST}:{OTREE_PORT}/api/sessions/{code}/participants",
    )
    return resp.json()


def advance_participant(code):
    requests.post(
        f"http://{OTREE_HOST}:{OTREE_PORT}/api/participants/{code}/advance",
    )
