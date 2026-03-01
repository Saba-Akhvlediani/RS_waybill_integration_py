from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from lxml import etree
import xml.etree.ElementTree as ET


WSDL = "https://services.rs.ge/WayBillService/WayBillService.asmx?WSDL"


class RsClient:

    def __init__(self, su, sp):

        self.su = su
        self.sp = sp
        self._history = HistoryPlugin()
        self._client = Client(wsdl=WSDL, plugins=[self._history])


    def _auth(self):

        return {
            "su": self.su,
            "sp": self.sp
        }

    def _get_raw_xml(self):
        # ვიღებთ ნედლ XML response envelope,XML-ს უბრალოდ ტექსტად გვაძლევს (read-only, debugging)

        envelope = self._history.last_received['envelope']
        return etree.tostring(envelope, pretty_print=True).decode()

    def _extract_xml_response(self, result_text):
        # ვაანალიზებთ(parse) XML სტრინგს რომელიც დაბრუნებულია და არის envelope-ის შიგნით,
        # XML ტექსტს პარსავს და გვაძლევს ობიექტს, რომ კოდით წავიკითხოთ

        if result_text is None:
            return None

        root = ET.fromstring(result_text)
        return root


    def _parse_table_rows(self, root):
        # ვაკონვერტირებთ XML rows მონაცემთა ცხრილს dict-ის სიად
        result = []
        for row in root.findall('Table'):
            row_dict = {}
            for field in row:
                row_dict[field.tag] = field.text
            result.append(row_dict)

        return result
        #envelope = self._history.last_received['envelope']

        # print the full raw XML so we can see the structure
        #print(etree.tostring(envelope, pretty_print=True).decode())

    def what_is_my_ip(self):
        return self._client.service.what_is_my_ip()

    def get_akciz_codes(self):
        return self._client.service.get_akciz_codes()

    def get_waybill_types(self):
        return self._client.service.get_waybill_types(**self._auth())


    def verify_credentials(self):
        try:
            result = self._client.service.chek_service_user(**self._auth())
            return result
        except Exception:
            return self._parse_datatable()
    # def get_ser_users(self):
    #     try:
    #         result = self._client.service.get_ser_users(
    #             user_name=self.su,
    #             user_password=self.sp
    #         )
    #         return result
    #     except Exception:
    #         return self._parse_datatable()

if __name__ == "__main__":
    rs_c = RsClient(su="ARCHIL", sp="12345")
    # print(rs_c.what_is_my_ip())
    # print(rs_c.verify_credentials())
    # print(rs_c.get_ser_users())
    # print(rs_c.get_akciz_codes())
    result = rs_c.get_waybill_types()
    print(ET.tostring(result, encoding='unicode'))

#
# result = Client.service.get_waybill_types(su="satesto2", sp="123456")
# print(ET.tostring(result, encoding='unicode'))