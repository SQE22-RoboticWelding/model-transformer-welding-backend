"""code_generator.py handles codegen of models."""
from typing import Dict
from jinja2 import Template
from app.schemas.generation_template import GenerationTemplate


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, values: Dict) -> str:
        return Template(template.content).render(values)
