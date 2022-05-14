"""ActionCache.py keeps in-memory information about Actions. THIS IS A TEMPORARY SOLUTION."""

from typing import Dict

from pydantic.schema import datetime

from model.ActionParameter import ActionParameter
from model.Action import Action
from model.ActionSequence import ActionSequence


class ActionCache:
    parameters: Dict[str, ActionParameter]
    actions: Dict[str, Action]
    action_sequence: Dict[str, ActionSequence]

    def __init__(self):
        self.parameters = {}
        self.actions = {}
        self.action_sequence = {}

    def fill_with_dummies(self):
        self.parameters["p1"] = ActionParameter("x", 5.5)
        self.parameters["p2"] = ActionParameter("y", 2.3)
        self.parameters["p3"] = ActionParameter("z", 4.1)
        self.parameters["p4"] = ActionParameter("pitch", 0.25)
        self.parameters["p5"] = ActionParameter("roll", 0.50)
        self.parameters["p6"] = ActionParameter("yaw", 0.75)

        self.actions["move_1"] = Action("move_1", list(self.parameters.values()))
        action = self.actions["move_1"]

        self.action_sequence["seq_1"] = ActionSequence("seq_1", None, datetime.now(), [action, action, action])
