import click
from tamu_crossref import XMLGenerator, PrefixLookup

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

@cli.command("find", help="Find TAMU DOIs")
@click.option(
    "--prefix",
    "-p",
    help="prefix to lookup",
    required=False,
    default="10.21423"
)
@click.option(
    "--mailto",
    "-m",
    help="Email address associated with request",
    required=True,
)
@click.option(
    "--output",
    "-o",
    help="Output csv file",
    required=False,
    default="output.csv",
)
def find(prefix: str, mailto: str, output: str) -> None:
    prefix = PrefixLookup(output=output, prefix=prefix, mail_to=mailto)
    prefix.write()
