from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES_PATH = Path(__file__).parent.parent / "assets" / "templates"
ENV = Environment(loader=FileSystemLoader(TEMPLATES_PATH))


def render_template(file_name: str, **kwargs) -> str:
    return ENV.get_template(file_name).render(**kwargs)
