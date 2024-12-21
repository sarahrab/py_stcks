from collections import namedtuple
from typing import List, Dict, Any, Optional

import yaml
from pydantic import BaseModel, TypeAdapter


class UserAction(BaseModel):
    action_key: str
    action_caption: str
    levels: List[int]
    levels_str: str


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
                    self.actions.append(UserAction(action_key=action[0], action_caption=action[1], levels_str=action[2]))

                # self.actions = TypeAdapter(List[UserAction]).validate_python(result)

        except Exception:
            self.actions = None

    def get_actions(self, level: int) -> List[UserAction]:
        result = []
        for action in self.actions:
            if action.levels is None or action.levels.count(level) > 0:
                result.append(action)
        return result

    def is_applicable(self, action: UserAction, level: int) -> bool:
        if action.levels_str is None or len(action.levels_str) == 0 or action.levels_str.startswith('ALL'):
            return True

        length = len(action.levels_str)
        apply = True
        if action.levels_str.startswith('NOT'):
            apply = False
            tail = action.levels_str[4:length - 1]
        else:
            tail = action.levels_str[1:length - 1]

        levels = tail.split(',')
        for l in levels:
            if l == str(level):
                return apply

        return not apply

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
