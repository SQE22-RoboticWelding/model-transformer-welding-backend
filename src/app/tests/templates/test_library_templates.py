from app.templates.getter import get_count_template_files, get_library_templates


def test_templates_load_library_templates():
    assert get_count_template_files() == len(get_library_templates())
