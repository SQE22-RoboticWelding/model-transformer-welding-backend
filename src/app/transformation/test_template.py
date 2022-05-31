import unittest
from typing import List

from requests import Request

from app.schemas.actions import action
from app.transformation import abstract_model, instance_model, template, code_generator

# prepare request object required for starlette-inbuilt jinja engine
request = Request(method="POST", url="127.0.0.1/test")


class TestTemplate(unittest.TestCase):
    meta: abstract_model.MetaInformation
    imports: List[List[str]]
    setup: abstract_model.Setup

    actions: List[abstract_model.Action]

    def setUp(self):
        # prepare test data
        self.meta = abstract_model.MetaInformation(language="python3", title="My Test Template", version="v0.0.1")
        self.imports = [["do this", "and this"], ["and that"]]
        self.setup = abstract_model.Setup(independent=["independent 1", "independent 2"],
                                          dependees=[abstract_model.Dependee(generated_reference="dependee",
                                                                             initializer="5")])

        param_1 = abstract_model.NamedParameter(abstract_name="abs_param1",
                                                generated_name="ins_param1",
                                                type=abstract_model.ParameterType.NUMBER,
                                                description="Descr 1")
        param_2 = abstract_model.NamedParameter(abstract_name="abs_param2",
                                                generated_name="ins_param2",
                                                type=abstract_model.ParameterType.STRING,
                                                description="Descr 2")
        action_1 = abstract_model.Action(abstract_name="action",
                                         generated_name="function",
                                         generated_actor="dependee",
                                         named_parameters=[param_1, param_2])
        action_2 = abstract_model.Action(abstract_name="dissatisfaction",
                                         generated_name="method",
                                         generated_actor="dependee",
                                         named_parameters=[param_2, param_1])
        self.actions = [action_1, action_2]

    def test_instantiate_action_all_empty(self):
        t = template.Template(meta=self.meta, init=[],
                              setup=abstract_model.Setup(independent=[], dependees=[]),
                              actions=[])
        model = instance_model.create_instance_model(t, [])
        response = code_generator.CodeGenerator.sequence_to_model(model, request)

        result = response.body.decode("utf-8")
        expect = ("\n"
                  "if __name__ == '__main__':\n"
                  "    return\n")

        self.assertEqual(expect, result)

    def test_instantiate_action_only_imports(self):
        t = template.Template(meta=self.meta, init=self.imports,
                              setup=abstract_model.Setup(independent=[], dependees=[]),
                              actions=[])
        model = instance_model.create_instance_model(t, [])
        response = code_generator.CodeGenerator.sequence_to_model(model, request)

        result = response.body.decode("utf-8")
        expect = ("do this\n"
                  "and this\n"
                  "\n"
                  "and that\n"
                  "\n"
                  "\n"
                  "if __name__ == '__main__':\n"
                  "    return\n")

        self.assertEqual(expect, result)

    def test_instantiate_action_only_init(self):
        t = template.Template(meta=self.meta, init=[],
                              setup=abstract_model.Setup(independent=["independent 1", "independent 2"], dependees=[]),
                              actions=[])
        model = instance_model.create_instance_model(t, [])
        response = code_generator.CodeGenerator.sequence_to_model(model, request)

        result = response.body.decode("utf-8")
        expect = ("\n"
                  "def init():\n"
                  "    independent 1\n"
                  "    independent 2\n"
                  "\n"
                  "    return\n"
                  "\n"
                  "\n"
                  "if __name__ == '__main__':\n"
                  "    init()\n"
                  "\n"
                  "    return\n")

        self.assertEqual(expect, result)

    def test_instantiate_action_only_run(self):
        for a in self.actions:
            a.generated_actor = None
        t = template.Template(meta=self.meta, init=[],
                              setup=abstract_model.Setup(independent=[], dependees=[]),
                              actions=self.actions)

        action_1_params = [action.ActionParameter("abs_param1", 5), action.ActionParameter("abs_param2", "5")]
        abstract_action_1 = action.Action("action", action_1_params)

        model = instance_model.create_instance_model(t, [abstract_action_1])
        response = code_generator.CodeGenerator.sequence_to_model(model, request)

        result = response.body.decode("utf-8")
        expect = ("\n"
                  "def run():\n"
                  "    function(ins_param1=5, ins_param2='5')\n"
                  "\n"
                  "\n"
                  "if __name__ == '__main__':\n"
                  "    run()\n"
                  "\n"
                  "    return\n")

        self.assertEqual(expect, result)

    def test_instantiate_action(self):
        t = template.Template(meta=self.meta, init=self.imports,
                              setup=self.setup,
                              actions=self.actions)

        action_1_params = [action.ActionParameter("abs_param1", 5), action.ActionParameter("abs_param2", "5")]
        abstract_action_1 = action.Action("action", action_1_params)

        action_2_params = [action.ActionParameter("abs_param2", "5"), action.ActionParameter("abs_param1", 5)]
        abstract_action_2 = action.Action("dissatisfaction", action_2_params)

        model = instance_model.create_instance_model(t, [abstract_action_1, abstract_action_2])

        response = code_generator.CodeGenerator.sequence_to_model(model, request)

        result = response.body.decode("utf-8")
        expect = ("do this\n"
                  "and this\n"
                  "\n"
                  "and that\n"
                  "\n"
                  "\n"
                  "def init():\n"
                  "    independent 1\n"
                  "    independent 2\n"
                  "\n"
                  "    return\n"
                  "\n"
                  "\n"
                  "def run(dependee):\n"
                  "    dependee.function(ins_param1=5, ins_param2='5')\n"
                  "    dependee.method(ins_param2='5', ins_param1=5)\n"
                  "\n"
                  "\n"
                  "if __name__ == '__main__':\n"
                  "    init()\n"
                  "\n"
                  "    dependee = 5\n"
                  "\n"
                  "    run(dependee)\n"
                  "\n"
                  "    return\n")

        self.assertEqual(expect, result)
