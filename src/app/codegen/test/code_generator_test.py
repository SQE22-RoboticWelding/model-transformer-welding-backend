import datetime
import unittest

from app.codegen.code_generator import CodeGenerator
from app.schemas.generation_template import GenerationTemplate


class CodeGeneratorTest(unittest.TestCase):
    template: GenerationTemplate

    def setUp(self) -> None:
        self.template = GenerationTemplate(id=1,
                                           name="My template",
                                           description="Description of my template",
                                           content="Hello, {{givenName}} {{familyName}}!",
                                           created_at=datetime.datetime.min,
                                           modified_at=datetime.datetime.max)

    def test_happy_case(self):
        result = CodeGenerator.generate(self.template, {"givenName": "Clive-Staples", "familyName": "Lewis"})
        expected = "Hello, Clive-Staples Lewis!"

        self.assertEqual(expected, result)
