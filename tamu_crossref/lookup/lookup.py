from habanero import Crossref
from csv import DictWriter


class PrefixLookup:
    def __init__(self, output="another_list_of_dois.csv", prefix="10.21423", mail_to=None):
        self.output = output
        self.prefix = prefix
        self.instance = self._set_instance(mail_to)
        self.records = self._lookup()

    @staticmethod
    def _set_instance(mail_to=None):
        return Crossref(mailto=mail_to) if mail_to else Crossref()

    def _lookup(self):
        all_records = []
        total_records = 7000
        offset = 0
        while offset < total_records:
            x = self.instance.prefixes(
                ids=self.prefix,
                works=True,
                limit=1000,
                offset=offset,
                sort="issued"
            )
            total_records = x['message']['total-results']
            for item in x['message']['items']:
                all_records.append(
                    {
                        "title": " | ".join(item.get('title', [''])),
                        "DOI": item['DOI'],
                        "URL": item['URL'],
                        "resource": item['resource']['primary']['URL'],
                        "indexed": item['indexed']['date-time'],
                        "type": item.get('type'),
                        "is-referenced-by-count": item.get('is-referenced-by-count', '0'),
                    }
                )
            offset += 1000
        return all_records

    def write(self):
        with open(self.output, 'w', newline='') as csvfile:
            fieldnames = ['title', 'DOI', 'URL', 'resource', 'indexed', 'type', 'is-referenced-by-count']
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.records)
