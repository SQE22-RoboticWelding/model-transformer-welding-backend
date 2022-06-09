"""code_generator.py handles codegen of models."""
from jinja2 import Template
from app.schemas.generation_template import GenerationTemplate
from app.models.welding_configuration import WeldingConfiguration


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, welding_configuration: WeldingConfiguration) -> str:
        return Template(template.content).render(welding_configuration.welding_points)
