from collections import namedtuple
from typing import List, Dict, Any, Optional

import yaml
from pydantic import BaseModel, TypeAdapter


class UserAction(BaseModel):
    action_key: str
    action_caption: str
    levels: List[int]


class ActionsModel(BaseModel):
    actions: Optional[List[UserAction]] | None = None

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.actions = []

    def initialize(self, filename: str):
        try:
            with open(filename, 'r') as file:
                result = yaml.safe_load(file)

                for e in result:
                    UA = namedtuple('UserAction', e.keys())
                    action = UA(**e)
                    self.actions.append(UserAction(action_key=action[0], action_caption=action[1], levels=action[2]))

                # self.actions = TypeAdapter(List[UserAction]).validate_python(result)

        except Exception:
            self.actions = None

    def get_actions(self, level: int) -> List[UserAction]:
        result = []
        for action in self.actions:
            if action.levels is None or action.levels.count(level) > 0:
                result.append(action)
        return result

# Yaml wtih List[user_action_def]

# user_actions:
# - action_key: check_funds
#   "Check Funds"
#   - levels
#       0
#       1

# - action_key: add_stock
#   "Add Stock"
#   - levels
#       0
# -
#
