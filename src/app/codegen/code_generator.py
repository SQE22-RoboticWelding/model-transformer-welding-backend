"""code_generator.py handles codegen of models."""
from jinja2 import Template
from app.schemas.generation_template import GenerationTemplate
from app.models.project import Project


class CodeGenerator:
    @staticmethod
    def generate(template: GenerationTemplate, project: Project) -> str:
        return Template(template.content).render({"welding_points": project.welding_points})
