import json
import unittest
from typing import List

from requests import Request


# prepare request object required for starlette-inbuilt jinja engine
from app.transformation.code_generator import CodeGenerator
from app.transformation.model_lowcode import ActionLowCode
from app.transformation.template import Template, Setup

request = Request(method="POST", url="127.0.0.1/test")


class TestTemplate(unittest.TestCase):
    template: Template
    actions: List[ActionLowCode]

    @classmethod
    def setUpClass(cls) -> None:
        cls.maxDiff = None
        # prepare test data
        with open("app/transformation/test/resources/template.json", "r") as f:
            cls.template = Template.parse_raw(f.read())

        with open("app/transformation/test/resources/actions.json", "r") as f:
            arr = json.load(f)
            cls.actions = [ActionLowCode.parse_obj(obj) for obj in arr]

    def test_instantiate_action(self):
        with open("app/transformation/test/resources/result.py", "r") as f:
            expect = f.read()
            response = CodeGenerator.generate(self.template, self.actions, request)
            result = response.body.decode("utf-8")

            self.assertEqual(expect, result)

    def test_instantiate_action_all_empty(self):
        with open("app/transformation/test/resources/result_all_empty.py", "r") as f:
            expect = f.read()
            template = self.template.copy(deep=True)
            template.init = []
            template.setup = Setup(independent=[], dependees=[])
            template.actions = []

            response = CodeGenerator.generate(template, [], request)
            result = response.body.decode("utf-8")

            self.assertEqual(expect, result)

    def test_instantiate_action_only_imports(self):
        with open("app/transformation/test/resources/result_only_imports.py", "r") as f:
            expect = f.read()
            template = self.template.copy(deep=True)
            template.setup = Setup(independent=[], dependees=[])
            template.actions = []

            response = CodeGenerator.generate(template, [], request)
            result = response.body.decode("utf-8")

            self.assertEqual(expect, result)

    def test_instantiate_action_only_setup(self):
        with open("app/transformation/test/resources/result_only_setup.py", "r") as f:
            expect = f.read()
            template = self.template.copy(deep=True)
            template.setup.dependees = []
            template.init = []
            template.actions = []

            response = CodeGenerator.generate(template, [], request)
            result = response.body.decode("utf-8")

            self.assertEqual(expect, result)

    def test_instantiate_action_only_run(self):
        with open("app/transformation/test/resources/result_only_run.py", "r") as f:
            expect = f.read()
            template = self.template.copy(deep=True)
            template.init = []
            template.setup = Setup(independent=[], dependees=[])
            for action in template.actions:
                action.generated_actor = None

            response = CodeGenerator.generate(template, self.actions, request)
            result = response.body.decode("utf-8")

            self.assertEqual(expect, result)
