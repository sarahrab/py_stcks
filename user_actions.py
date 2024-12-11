from typing import List

from pydantic import BaseModel


class user_action_def(BaseModel):
    action_key: str
    action_caption: str
    levels: List[int]

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
#

