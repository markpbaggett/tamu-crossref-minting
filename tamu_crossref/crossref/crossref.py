from csv import DictReader
from lxml import etree
from lxml.builder import ElementMaker
from datetime import datetime


class XMLGenerator:
    """Class to generate XML documents from XML elements"""
    def __init__(self, csv_file, email, name, type_of_deposit):
        self.csv_file = csv_file
        self.email = email
        self.name = name
        self.csv_contents = self.__read_csv()
        self.xml = self.construct_xml(type_of_deposit)

    def __read_csv(self):
        with open(self.csv_file, "r") as file:
            reader = DictReader(file)
            return [row for row in reader]

    def construct_xml(self, deposit_type):
        head = Head(self.email, self.name)
        body = Body(self.csv_contents, deposit_type)
        xml = CrossrefXML(head.head_xml, body.body_xml)
        return xml.xml

    def write_xml(self, output_file):
        with open(output_file, "wb") as file:
            file.write(
                etree.tostring(
                    self.xml, pretty_print=True, xml_declaration=True, encoding="UTF-8"
                )
            )


class CrossrefElement:
    """Base class for crossref elements"""
    def __init__(self):
        self.cr = self._build_namespace("http://www.crossref.org/schema/5.3.1", None)
        self.xsi = self._build_namespace(
            "http://www.w3.org/2001/XMLSchema-instance", "xsi"
        )
        self.jats = self._build_namespace(
            "http://www.ncbi.nlm.nih.gov/JATS1", "jats"
        )
        self.mml = self._build_namespace(
            "http://www.w3.org/1998/Math/MathML", "mml"
        )

    @staticmethod
    def _build_namespace(uri, short):
        return ElementMaker(
            namespace=uri,
            nsmap={
                short: uri,
            },
        )


class Head(CrossrefElement):
    def __init__(
        self,
        email,
        name,
        registrant="Texas A&M University Libraries",
    ):
        super().__init__()
        self.email = email
        self.name = name
        self.head_xml = self.create(registrant)

    def create(self, registrant):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return self.cr.head(
            self.cr.doi_batch_id(f"TAMU_Libraries_{timestamp}"),
            self.cr.timestamp(timestamp),
            self.cr.depositor(
                self.cr.depositor_name(self.name), self.cr.email_address(self.email)
            ),
            self.cr.registrant(
                registrant
            ),
        )


class CrossrefXML(CrossrefElement):
    """Class to handle creation of the main XML document"""
    def __init__(self, head, body):
        super().__init__()
        self.head = head
        self.body = body
        self.xml = self.create()

    def create(self):
        begin = self.cr.doi_batch(self.head, self.body)
        begin.attrib["{http://www.w3.org/2001/XMLSchema-instance}schemaLocation"] = (
            "http://www.crossref.org/schema/5.3.1 http://www.crossref.org/schemas/crossref5.3.1.xsd"
        )
        begin.attrib["version"] = "5.3.1"
        return begin


class Body(CrossrefElement):
    def __init__(self, items, type_of_deposit):
        super().__init__()
        self.items = items
        self._validate_deposit_type(type_of_deposit)
        self.type_of_deposit = type_of_deposit
        self.body_xml = self.create()

    @staticmethod
    def _validate_deposit_type(deposit_type):
        supported_types = ("reports")
        if deposit_type not in supported_types:
            raise ValueError(f"{deposit_type} is not a valid deposit type")
        return

    def create(self):
        if self.type_of_deposit == "reports":
            return self.cr.body(
                *self.add_papers()
            )

    def add_papers(self):
        all_papers = []
        for paper in self.items:
            new_report = ReportPaper(paper)
            all_papers.append(new_report.xml)
        return all_papers


class ReportPaper(CrossrefElement):
    def __init__(self, paper):
        super().__init__()
        self.paper = paper
        self.xml = self.create()

    def create(self):
        return (
            # @TODO: Make Subelements reusable
            self.cr.__call__(
                "report-paper",
                self.cr.__call__(
                    "report-paper_metadata",
                    ContributorList(self.paper["contributors"]).contributor_xml,
                    self.cr.titles(
                        self.cr.title(
                            self.paper["title"]
                        )
                    ),
                    self.jats.abstract(
                        self.jats.p(
                            self.paper["abstract"]
                        )
                    ),
                    self.cr.publication_date(
                        self.cr.month(
                            self.paper["publication_date"].split("-")[1]
                        ),
                        self.cr.day(
                            self.paper["publication_date"].split("-")[2]
                        ),
                        self.cr.year(
                            self.paper["publication_date"].split("-")[0]
                        ),
                        media_type="online"
                    ),
                    # @TODO: Don't assume publisher details
                    self.cr.publisher(
                        self.cr.publisher_name(
                            "Southwest Rural Health Research Center, Texas A&amp;M School of Public Health"
                        ),
                        self.cr.publisher_place(
                            "College Station, TX"
                        )
                    ),
                    self.cr.doi_data(
                        self.cr.doi(
                            self.paper["doi"]
                        ),
                        self.cr.resource(
                            self.paper["identifier"]
                        )
                    ),
                    language='en'
                ),
                publication_type="full_text"
            )
        )


class ContributorList(CrossrefElement):
    def __init__(self, contributors):
        super().__init__()
        self.contributors = contributors.split(" | ")
        self.contributor_xml = self.create()

    def create(self):
        return self.cr.contributors(*self.add_contributors())

    def add_contributors(self):
        all_contributors = []
        i = 0
        for contributor in self.contributors:
            surname = contributor.split(",")[0].strip()
            given_name = contributor.split(",")[1].strip()
            if i == 0:
                sequence = "first"
            else:
                sequence = "additional"
            contributor_xml = self.cr.person_name(
                self.cr.given_name(given_name),
                self.cr.surname(surname),
                contributor_role="author",
                sequence=sequence
            )
            all_contributors.append(contributor_xml)
            i += 1
        return all_contributors

