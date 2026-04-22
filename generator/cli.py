from pathlib import Path

import click
import click_log

from .csv_analyzer import analyze_csv
from .code_generator import CodeGenerator

import logging

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


# @click.group()
# def cli():
#     """CSV to Python dataclass code generator."""
#     pass


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--output', '-o', default='output',
    help='Output directory for generated files. "-" outputs the result to stdout.'
)
@click.option('--sample-size', '-s', default=256, help='Number of rows to sample for type inference')
@click.option(
    '--name', '-n', default=None,
    help='Alternative name for the generated name. Snake case / spaced words is recommended.',
)
def generate(input_file, output, sample_size, name):
    """Generate dataclass and loader code from CSV files."""
    schema = analyze_csv(Path(input_file), sample_size, base_name=name)
    if len(schema.duplicated_fields):
        logger.warning(f"CSV file {input_file} contains duplicated fields. Data retrieved from CSV may be incorrect.")
        logger.warning(f"Duplicated fields: [{', '.join(schema.duplicated_fields)}]")
    generator = CodeGenerator(
        schema=schema,
        output_dir=output,
    )
    generator.generate_and_write_code()
    pass


if __name__ == '__main__':
    generate()
