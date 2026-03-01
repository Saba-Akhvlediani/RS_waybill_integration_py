from zeep import Client      # reads the wsdl, builds python methods automatically
from zeep.exceptions import Fault
from datetime import datetime
import logging
from dataclasses import dataclass
from typing import Optional
from xml.etree import ElementTree as ET   #



logger = logging.getLogger(__name__)

#wsdl - web service description language
WSDL = "https://services.rs.ge/WayBillService/WayBillService.asmx?WSDL"

class WaybillType:
    INTERNAL_TRANSPORT = 1
    WITH_TRANSPORT = 2
    WITHOUT_TRANSPORT = 3
    DISTRIBUTION = 4
    SUB_WAYBILL = 6
    RETURN = 5

class CitizenCheck:
    FOREIGNER = 0
    GEORGIAN = 1


class VatType:
    STANDARD = 0
    ZERO = 1
    EXEMPT = 2

class WaybillStatus:
    SAVED = 0
    ACTIVE = 1
    COMPLETED = 2
    SENT_TO_CARRIER = 8
    DELETED = -1
    CANCELED = -2

class TransportCostPayer:
    BUYER = 1
    SELLER = 2


client = Client(wsdl="https://services.rs.ge/WayBillService/WayBillService.asmx?WSDL")


print(client.wsdl.dump())
result = client.service.chek('ARCHIL', '12345',135184)

print(result)


# print(client.service.what_is_my_ip())

# class RSgeClient:
#
#     def __init__(self, su, sp, user_id, un_id):
#         self.su = su
#         self.sp = sp
#         self.user_id = user_id
#         self.un_id = un_id
#
#         self._client = Client(client)
#
#
#     def auth(self):
#         pass
#
#     def what_is_my_ip(self):
#
#         self._client.service.what_is_my_ip()
#
#
#
# if __name__ == '__main__':
#     client = RSgeClient("su", "sp", "user", "un")
#
#     print(client.what_is_my_ip())
