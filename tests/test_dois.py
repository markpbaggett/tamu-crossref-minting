import os
from lxml import etree
import pytest
from pathlib import Path

schemas_path = Path(__file__).parent / "test_schemas"
schemas_copies = Path(__file__).parent / "schema_copies"
SCHEMAS = f"{schemas_path}/schemas.xsd"
DOI_FILES = "dois"

class CustomResolver(etree.Resolver):
    def resolve(self, url, id, context):
        mapping = {
            "../schema_copies/crossref531.xsd": f"{schemas_copies}/crossref531.xsd",
            "../schema_copies/mathml3.xsd": f"{schemas_copies}/mathml3.xsd",
            "../schema_copies/relations.xsd": f"{schemas_copies}/relations.xsd",
        }
        if url in mapping:
            return self.resolve_filename(mapping[url], context)
        return None

@pytest.fixture
def custom_parser():
    """Fixture to provide an XMLParser with a CustomResolver."""
    parser = etree.XMLParser()
    parser.resolvers.add(CustomResolver())
    return parser

@pytest.fixture
def master_schema(custom_parser):
    """Fixture to load the master schema with the custom parser."""
    schema_path = f"{schemas_path}/schemas.xsd"
    with open(schema_path, "rb") as schema_file:
        schema_doc = etree.parse(schema_file, custom_parser)
        return etree.XMLSchema(schema_doc)

@pytest.mark.parametrize("xml_file", [
    pytest.param(filename, id=filename)
    for filename in os.listdir(DOI_FILES)
    if filename.endswith(".xml")
])
def test_validate_xml(master_schema, xml_file):
    """Test that XML files validate against the master schema."""
    filepath = os.path.join(DOI_FILES, xml_file)
    with open(filepath, "rb") as file:
        xml_doc = etree.parse(file)
        try:
            master_schema.assertValid(xml_doc)
            print(f"{filepath} is valid.")
        except etree.DocumentInvalid as e:
            pytest.fail(f"{filepath} is invalid: {e}")
