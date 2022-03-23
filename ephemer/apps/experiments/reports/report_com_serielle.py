import csv
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render as dj_render


def render(request, session) -> HttpResponse:

    initial_message = ""
    groups = defaultdict(dict)

    with open(session.csv, "r") as csv_file:

        csv_reader = csv.reader(csv_file)
        title_row = csv_reader.__next__()
        columns_index = {value: index for index, value in enumerate(title_row)}

        for row in csv_reader:
            if not initial_message:
                row_initial_message = row[columns_index["group.initial_message"]]
                if row_initial_message:
                    initial_message = row_initial_message

            row_message = row[columns_index["group.message"]]
            if not row_message:
                continue

            group_id = row[columns_index["group.id_in_subsession"]]
            round_number = row[columns_index["subsession.round_number"]]
            if round_number not in groups[group_id]:
                groups[group_id][round_number] = row_message

    groups_for_context = []
    groups_counter = 1
    for messages_dict in groups.values():
        round_numbers = sorted(messages_dict.keys())
        groups_for_context.append(
            {
                "id": groups_counter,
                "messages": [
                    {"compte_relais": nb, "texte": messages_dict[nb]}
                    for nb in round_numbers
                ],
            }
        )
        groups_counter += 1

    context = {
        "session": session,
        "groups": groups_for_context,
        "initial_message": initial_message,
    }
    return dj_render(request, "experiments/com_serielle_results.html", context)
