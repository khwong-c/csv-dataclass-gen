"""Code generation orchestrator using Jinja2 templates."""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

import contextlib
import sys

from .csv_analyzer import CSVSchema


@contextlib.contextmanager
def open_file_or_stdout(output_dir: Path | None, filename: str):
    if output_dir is None:
        yield sys.stdout
    else:
        with (output_dir / filename).open('w') as f:
            yield f


class CodeGenerator:
    """Generate Python code from CSV schemas using Jinja2 templates."""

    def __init__(
            self, schema: CSVSchema,
            output_dir: str,
    ):
        """
        Initialize code generator.

        Args:
            schema: CSVSchema with column information
        """
        self.schema = schema
        self.output_dir = Path(output_dir) if output_dir != '-' else None

        template_dir = Path(__file__).parent / 'templates'
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=False
        )

    def generate_dataclass_code(self) -> str:
        """
        Generate dataclass + loader function code.

        Returns:
            Generated Python code as string
        """
        template = self.env.get_template('dataclass_template.py.jinja2')
        schema = self.schema

        # Prepare context for template rendering
        context = {
            'class_name': schema.class_name,
            'function_name': schema.function_name,
            'filename': schema.file_name,
            'delimiter': schema.delimiter,
            'columns': schema.columns,
        }

        return template.render(context)

    def generate_and_write_code(self):
        if self.output_dir is not None:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        with open_file_or_stdout(
                self.output_dir, f"{self.schema.module_name}.py",
        ) as f:
            f.write(self.generate_dataclass_code())
