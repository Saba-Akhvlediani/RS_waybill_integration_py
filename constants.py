from enum import IntEnum


class WaybillType(IntEnum):

    INTERNAL_TRANSPORT = 1
    WITH_TRANSPORT = 2
    WITHOUT_TRANSPORT = 3
    DISTRIBUTION = 4
    RETURN = 5
    SUB_WAYBILL = 6


class WaybillStatus(IntEnum):

    SAVED = 0
    ACTIVE = 1
    COMPLETED = 2
    SENT_TO_TRANSPORTER = 8
    DELETED = -1
    CANCELED = -2

class WaybillCategory(IntEnum):

    NORMAL = 0
    WOOD = 1

class VatType(IntEnum):

    STANDARD = 0
    ZERO = 1
    EXEMPT = 2


class CitizenCheck(IntEnum):

    FOREIGNER = 0
    GEORGIAN = 1


class TransportCostPayer(IntEnum):

    BUYER = 1
    SELLER = 2


class IsMedicine(IntEnum):

    NORMAL = 0
    MEDICINE = 1


class CustomsStatus(IntEnum):

    CONFIRMED = 1
    REJECTED = 2


class IsConfirmed(IntEnum):

    UNCONFIRMED = 0
    CONFIRMED = 1
    REJECTED = 2

class BuyerStatus(IntEnum):

    WITHOUT_STATUS = 0
    MICRO_BUSINESS_STATUS = 1
    SMALL_BUSINESS_STATUS = 2


class PayerType(IntEnum):
    PHYSICAL_PERSON = 1
    LEGAL_ENTITY = 2
    INDIVIDUAL_ENTREPRENEUR = 3


class TransportType(IntEnum):
    AUTO = 1
    RAILWAY = 2
    AIR = 3
    OTHER = 4
