import os
import json
from pathlib import Path
from typing import List

from app.schemas.generation_template import LibraryTemplate

__path_to_templates = Path(__file__).parent


def __get_templates_in_path() -> List[bytes]:
    templates = []
    for path in os.listdir(__path_to_templates):
        filepath = os.path.join(__path_to_templates, path)
        if os.path.isfile(filepath) and path.split(".")[-1] == "template": # noqa
            templates.append(filepath)
    return templates


def get_count_template_files() -> int:
    return len(__get_templates_in_path())


def get_library_templates() -> List[LibraryTemplate]:
    library_templates = []
    for template in __get_templates_in_path():
        with open(template, "r") as f:
            try:
                content = f.readlines()
                # First line contains JSON string with metadata
                json_obj = json.loads(content[0])

                # Remaining lines are the template
                content = content[1:]
                json_obj["content"] = "".join(content)

                library_templates.append(LibraryTemplate(**json_obj))
            except Exception as e: # noqa (PEP E722)
                # no exception is (re-)thrown as the failure to read a library template is limited relevance
                print(f"Template file '{os.path.basename(template)}' cannot be loaded: {e}")

    return library_templates
