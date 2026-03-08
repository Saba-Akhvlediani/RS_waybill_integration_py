from zeep import Client
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from lxml import etree
import xml.etree.ElementTree as ET
from xml_parser import XmlParser
from xml_builder import XmlBuilder
from datetime import datetime, timedelta

WSDL = "https://services.rs.ge/WayBillService/WayBillService.asmx?WSDL"


class RsClient:

    def __init__(self, su, sp):

        self.su = su
        self.sp = sp

        """historyplugin ინახავს ბოლო request/response xml-ს,
        გვჭირდება რადგან zeep ვერ პარსავს rs.ge მონაცემთა ცხრილის response-ს"""
        self._history = HistoryPlugin()
        self._client = Client(wsdl=WSDL, plugins=[self._history])

        self._parser = XmlParser()
        self._builder = XmlBuilder()


    def _auth(self):
        return  self._builder.build_auth(self.su, self.sp)


    def _last_envelope(self):
        return self._history.last_received['envelope']


    def _call_datatable(self, method_name, params, row_tag='Table'):
        """
        ეს მეთოდი გამოიყენება გვაძლევს საშუალებას გამოვიძახოთ ნებისმიერი მეთოდი რომელიც მონაცემთა ცხრილს აბრუნებს
        zeep ვერ გაპარსავს ამიტომ იძახებს parser ფუნქციას
        """
        try:
            getattr(self._client.service, method_name)(**params)

        except Exception:
            pass
        return self._parser.parse_datatable(self._last_envelope(),row_tag)


    def what_is_my_ip(self):
        return self._client.service.what_is_my_ip()


    def get_server_time(self):
        return self._client.service.get_server_time()


    # def get_service_users(self, user_name, user_password):
    #
    #     return self._call_datatable(
    #         method_name='get_service_users',
    #         params={'user_name': user_name, 'user_password': user_password},
    #         row_tag='ServiceUser',
    #     )

    def get_service_users(self):

        return self._call_datatable(method_name='get_service_users', params={
            'user_name': self.su,
            'user_password': self.sp
        }, row_tag='ServiceUser')


    def verify_credentials(self):

        result = self._client.service.chek_service_user(**self._auth())
        return {
            'valid': result.chek_service_userResult,
            'un_id': result.un_id,
            's_user_id': result.s_user_id,
        }


    def get_name_from_tin(self, tin):
        """TIN-ით კომპანიის/პირის სახელის მიღება."""

        result = self._client.service.get_name_from_tin(tin=tin,**self._auth())
        return result.get_name_from_tinResult


    def get_tin_from_un_id(self, un_id):
        """RS.GE unique ID → TIN და სახელი."""

        result = self._client.service.get_tin_from_un_id(un_id=un_id,**self._auth())

        return {
            'tin': result.get_tin_from_un_idResult,
            'name': result.name,
        }

    def is_vat_payer_tin(self, tin):
        """კომპანია (TIN-ით) დღგ-ის გადამხდელია თუ არა."""

        result = self._client.service.is_vat_payer_tin(tin=tin,**self._auth())
        return result.is_vat_payer_tinResult


    def get_waybill_types(self):
        """ზედნადების ტიპების სია (სტანდარტული, შიდა, დაბრუნება...)."""
        return self._call_datatable('get_waybill_types', self._auth())


    def get_waybill_units(self):
        """საზომი ერთეულების სია (კგ, ცალი, ლიტრი...)."""
        return self._call_datatable('get_waybill_units', self._auth())


    def get_trans_types(self):
        """ტრანსპორტის ტიპების სია (ავტო, სარკინიგზო, საჰაერო...)."""
        return self._call_datatable('get_trans_types', self._auth())


    def get_error_codes(self):
        """RS.GE-ს შეცდომის კოდების და აღწერილობების სია."""
        return self._call_datatable('get_error_codes', self._auth())


    def save_waybill(self, seller_tin, buyer_tin, start_address, end_address, driver_tin, car_number,waybill_type,
                     transport_type, goods):

        waybill_xml = self._builder.build_waybill(
            seller_tin=seller_tin,
            buyer_tin=buyer_tin,
            start_address=start_address,
            end_address=end_address,
            driver_tin=driver_tin,
            car_number=car_number,
            waybill_type=waybill_type,
            transport_type=transport_type,
            goods=goods
        )

        try:
            result = self._client.service.save_waybill(su=self.su, sp=self.sp, waybill=waybill_xml)
            return result
        except Exception:
            self._parser.print_raw(self._last_envelope())
            raise


    def send_waybill(self, waybill_id):
        result = self._client.service.send_waybill(waybill_id=waybill_id,**self._auth())

        return result.send_waybillResult


    def send_waybill_with_date(self, waybill_id, begin_date):
        result = self._client.service.send_waybil_vd(
            waybill_id=waybill_id,
            begin_date=begin_date,
            **self._auth()
        )

        return result.send_waybil_vdResult



    def close_waybill(self, waybill_id):
        result = self._client.service.close_waybill(waybill_id=waybill_id,**self._auth())

        return result.close_waybillResult



    def close_waybill_with_date(self, waybill_id, delivery_date):
        """ზედნადების დახურვა და კონკრეტული დროის მინიჭება"""
        result = self._client.service.close_waybill_vd(
            waybill_id=waybill_id,
            delivery_date=delivery_date,
            **self._auth(),
        )

        return result.close_waybill_vdResult



    def refuse_waybill(self, waybill_id):
        """უარყო/დააბრუნო ზედნადები (მყიდველი უარყოფს მიწოდებას)."""
        result = self._client.service.ref_waybill(
            waybill_id=waybill_id,
            **self._auth(),
        )

        return result.ref_waybillResult



    def refuse_waybill_with_comment(self, waybill_id, comment):
        """უარყო ზედნადები და დაამატო მიზეზი"""
        result = self._client.service.ref_waybill_vd(
            waybill_id=waybill_id,
            comment=comment,
            **self._auth(),
        )

        return result.ref_waybill_vdResult



    def delete_waybill(self, waybill_id):
        """ draft ზედნადების წაშლა (მოქმედებს მხოლოდ გაგზავნამდე)."""
        result = self._client.service.del_waybill(
            waybill_id=waybill_id,
            **self._auth(),
        )

        return result.del_waybillResult



    def confirm_waybill(self, waybill_id):
        """მყიდველი ადასტურებს ზედნადებს"""
        result = self._client.service.confirm_waybill(
            waybill_id=waybill_id,
            **self._auth(),
        )

        return result.confirm_waybillResult


    def reject_waybill(self, waybill_id):
        """მყიდველი  უარყოფს ზედნადებს"""
        result = self._client.service.reject_waybill(
            waybill_id=waybill_id,
            **self._auth(),
        )
        return result.reject_waybillResult


    def get_waybill(self, waybill_id):
        return self._call_datatable('get_waybill', {'waybill_id': waybill_id, **self._auth()},)



    def get_waybills(self, start_date, end_date,
                     buyer_tin='', statuses=''):
        """ყველა ზედნადები სადაც ჩვენ გამყიდველი ვართ."""
        params = self._builder.build_get_waybills(
            su=self.su,
            sp=self.sp,
            start_date=start_date,
            end_date=end_date,
            buyer_tin=buyer_tin,
            statuses=statuses,
        )
        return self._call_datatable('get_waybills', params)


    def get_buyer_waybills(self, start_date, end_date, seller_tin='', statuses=''):
        params = self._builder.build_get_buyer_waybills(
            su=self.su,
            sp=self.sp,
            start_date=start_date,
            end_date=end_date,
            seller_tin=seller_tin,
            statuses=statuses,
        )

        return self._call_datatable('get_buyer_waybills', params)


    def get_waybills_v1(self, last_update_start, last_update_end, buyer_tin=''):

        return self._call_datatable('get_waybills_v1', {
            'su': self.su,
            'sp': self.sp,
            'buyer_tin': buyer_tin,
            'last_update_start': last_update_start,
            'last_update_end': last_update_end,
        })

    def get_print_pdf(self, waybill_id):
        result = self._client.service.get_print_pdf(waybill_id=waybill_id, **self._auth())

        return result.get_print_pdfResult


if __name__ == "__main__":

    discovery_client = RsClient(su='tbilisi', sp='123456')
    print(discovery_client.what_is_my_ip())

    users = discovery_client.get_service_users()
    print("ip - is shezgudvis gareshe")
    for user in users:
        if not user.get('IP'):
            print(f" su={user['USER_NAME'].split(':')[0]} sp={user.get('NAME', 'N/A')}")


    # aqamde amoviget sub-userebi tavisi su da sp-it axla shevqmnit clients swori credentialebit
    client = RsClient(su='გიორგი', sp='Giorgi12345.')
    print(client.verify_credentials())

    for row in client.get_waybill_types():
        print(row)

    waybills = client.get_waybills(
        start_date=datetime.now() - timedelta(days=30),
        end_date=datetime.now(),
    )
    for w in waybills[:3]:
        print(w)



# if __name__ == "__main__":
#
#     # get all users without IP restriction and with a password
#     discovery = RsClient(su='tbilisi', sp='123456')
#     users = discovery.get_service_users()
#
#     candidates = [
#         u for u in users
#         if not u.get('IP') and u.get('NAME')
#     ]
#
#     print(f"Testing {len(candidates)} candidates...\n")
#
#     for user in candidates:
#         su = user['USER_NAME'].split(':')[0]
#         sp = user['NAME']
#
#         try:
#             client = RsClient(su=su, sp=sp)
#             result = client.verify_credentials()
#
#             if result['valid']:
#                 print(f"✓ WORKS!  su={su}  sp={sp}")
#                 print(f"  un_id={result['un_id']}  s_user_id={result['s_user_id']}")
#                 print("\n  Waybill types:")
#                 for row in client.get_waybill_types():
#                     print(f"    {row}")
#                 break  # stop at first working one
#             else:
#                 print(f"✗ Failed  su={su}  (un_id={result['un_id']})")
#
#         except Exception as e:
#             print(f"✗ Error   su={su}  → {e}")