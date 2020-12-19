from core.models import CoreEnum


class PaymentTypeEnum(str, CoreEnum):
    NAKIT = 'Nakit'
    CEK = 'Çek'
    KREDI_KARTI = 'Kredi Kartı'
    ACIK_HESAP = 'Açık Hesap'


class OrderTypeEnum(str, CoreEnum):
    STANDART = 'STANDART'
    ANT_FUAR_2020 = 'ANT_FUAR_2020'


class DeliveryTypeEnum(str, CoreEnum):
    OPEN = "Açık"
    READY = "Hazır"
    CLOSED = "Kapalı"
    DELIVERED = "Teslim_Edildi"

class OrderStateEnum(str, CoreEnum):
    OPEN = "Açık"
    CLOSED = "Kapalı"


