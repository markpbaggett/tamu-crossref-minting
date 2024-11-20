from tamu_crossref import XMLGenerator
import click

@click.group()
def cli() -> None:
    pass

@cli.command("generate", help="Generate Crossref XML from a CSV.")
@click.option(
    "--csv",
    "-c",
    help="Base CSV File",
    required=True,
)
@click.option(
    "--deposit_type",
    "-d",
    help="Type of deposit",
    type=click.Choice(['reports']),
    required=True,
)
@click.option(
    "--output",
    "-o",
    help="Output XML file",
    required=False,
    default="crossref.xml",
)
def generate(csv: str, deposit_type: str, output: str) -> None:
    x = XMLGenerator(
        csv_file=csv,
        email="mark.baggett@tamu.edu",
        name="Mark Baggett",
        type_of_deposit=deposit_type,
    )
    x.write_xml(output)
