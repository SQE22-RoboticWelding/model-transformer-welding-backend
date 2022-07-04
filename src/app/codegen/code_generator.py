"""code_generator.py handles codegen of models."""
from typing import List

from jinja2 import Template

from app.models.welding_point import WeldingPoint
from app.schemas.generation_template import GenerationTemplate
from app.models.project import Project


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, welding_points: List[WeldingPoint]) -> str:
        return Template(template.content, keep_trailing_newline=True).render({"welding_points": welding_points})
