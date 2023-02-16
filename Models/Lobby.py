
"""
lobby model

    name
    max_user_count
    cur_user_count
    creator
    organization(this will be ikea etc. or metafuar in games)
    users: []
"""

from datetime import datetime


class Lobby:
    def __init__(self, apiobj):
        self.name = apiobj["name"]
        self.max_user_count = apiobj["max_user_count"]
        self.organization = apiobj["organization"]
        self.creator = apiobj["creator"]
        self.users = []
        self.cur_user_count = 0
        self.creation_date = datetime.now()

