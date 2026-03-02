import xml.etree.ElementTree as ET
from lxml import etree



class XmlParser:


    def _envelope_to_root(self, envelope):

        raw_xml = etree.tostring(envelope).decode()

        return ET.fromstring(raw_xml)


    def parse_datatable(self, envelope, row_tag='Table'):

        root = self._envelope_to_root(envelope)
        rows = root.findall(f'.//{row_tag}')

        result = []
        for row in rows:
            row_dict = {field.tag: field.text for field in row}
            result.append(row_dict)

        return result


    def parse_single(self, envelope, row_tag='Table'):

        rows = self.parse_datatable(envelope, row_tag)
        return rows[0] if rows else None


    def print_raw(self, envelope):

        print(etree.tostring(envelope, pretty_print=True).decode())