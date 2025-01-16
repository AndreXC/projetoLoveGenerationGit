from typing import Any, List, TypeVar, Type, cast, Callable
from datetime import datetime



T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x




class Urls:
    failure: str
    pending: str
    success: str

    def __init__(self, failure: str, pending: str, success: str) -> None:
        self.failure = failure
        self.pending = pending
        self.success = success

    @staticmethod
    def from_dict(obj: Any) -> 'Urls':
        assert isinstance(obj, dict)
        failure = from_str(obj.get("failure"))
        pending = from_str(obj.get("pending"))
        success = from_str(obj.get("success"))
        return Urls(failure, pending, success)

    def to_dict(self) -> dict:
        result: dict = {}
        result["failure"] = from_str(self.failure)
        result["pending"] = from_str(self.pending)
        result["success"] = from_str(self.success)
        return result


class Metadata:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'Metadata':
        assert isinstance(obj, dict)
        return Metadata()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Payer:
    phone: Metadata
    address: Metadata
    email: str
    identification: Metadata
    name: str
    surname: str
    date_created: None
    last_purchase: None

    def __init__(self, phone: Metadata, address: Metadata, email: str, identification: Metadata, name: str, surname: str, date_created: None, last_purchase: None) -> None:
        self.phone = phone
        self.address = address
        self.email = email
        self.identification = identification
        self.name = name
        self.surname = surname
        self.date_created = date_created
        self.last_purchase = last_purchase

    @staticmethod
    def from_dict(obj: Any) -> 'Payer':
        assert isinstance(obj, dict)
        phone = Metadata.from_dict(obj.get("phone"))
        address = Metadata.from_dict(obj.get("address"))
        email = from_str(obj.get("email"))
        identification = Metadata.from_dict(obj.get("identification"))
        name = from_str(obj.get("name"))
        surname = from_str(obj.get("surname"))
        date_created = from_none(obj.get("date_created"))
        last_purchase = from_none(obj.get("last_purchase"))
        return Payer(phone, address, email, identification, name, surname, date_created, last_purchase)

    def to_dict(self) -> dict:
        result: dict = {}
        result["phone"] = to_class(Metadata, self.phone)
        result["address"] = to_class(Metadata, self.address)
        result["email"] = from_str(self.email)
        result["identification"] = to_class(Metadata, self.identification)
        result["name"] = from_str(self.name)
        result["surname"] = from_str(self.surname)
        result["date_created"] = from_none(self.date_created)
        result["last_purchase"] = from_none(self.last_purchase)
        return result


class PaymentMethods:
    default_card_id: None
    default_payment_method_id: None
    excluded_payment_methods: List[Any]
    excluded_payment_types: List[Any]
    installments: None
    default_installments: None

    def __init__(self, default_card_id: None, default_payment_method_id: None, excluded_payment_methods: List[Any], excluded_payment_types: List[Any], installments: None, default_installments: None) -> None:
        self.default_card_id = default_card_id
        self.default_payment_method_id = default_payment_method_id
        self.excluded_payment_methods = excluded_payment_methods
        self.excluded_payment_types = excluded_payment_types
        self.installments = installments
        self.default_installments = default_installments

    @staticmethod
    def from_dict(obj: Any) -> 'PaymentMethods':
        assert isinstance(obj, dict)
        default_card_id = from_none(obj.get("default_card_id"))
        default_payment_method_id = from_none(obj.get("default_payment_method_id"))
        excluded_payment_methods = from_list(lambda x: x, obj.get("excluded_payment_methods"))
        excluded_payment_types = from_list(lambda x: x, obj.get("excluded_payment_types"))
        installments = from_none(obj.get("installments"))
        default_installments = from_none(obj.get("default_installments"))
        return PaymentMethods(default_card_id, default_payment_method_id, excluded_payment_methods, excluded_payment_types, installments, default_installments)

    def to_dict(self) -> dict:
        result: dict = {}
        result["default_card_id"] = from_none(self.default_card_id)
        result["default_payment_method_id"] = from_none(self.default_payment_method_id)
        result["excluded_payment_methods"] = from_list(lambda x: x, self.excluded_payment_methods)
        result["excluded_payment_types"] = from_list(lambda x: x, self.excluded_payment_types)
        result["installments"] = from_none(self.installments)
        result["default_installments"] = from_none(self.default_installments)
        return result


class Shipments:
    default_shipping_method: None
    receiver_address: Metadata

    def __init__(self, default_shipping_method: None, receiver_address: Metadata) -> None:
        self.default_shipping_method = default_shipping_method
        self.receiver_address = receiver_address

    @staticmethod
    def from_dict(obj: Any) -> 'Shipments':
        assert isinstance(obj, dict)
        default_shipping_method = from_none(obj.get("default_shipping_method"))
        receiver_address = Metadata.from_dict(obj.get("receiver_address"))
        return Shipments(default_shipping_method, receiver_address)

    def to_dict(self) -> dict:
        result: dict = {}
        result["default_shipping_method"] = from_none(self.default_shipping_method)
        result["receiver_address"] = to_class(Metadata, self.receiver_address)
        return result


class TJSONGetProduto:
    additional_info: str
    auto_return: str
    back_urls: Urls
    binary_mode: bool
    client_id: str
    collector_id: int
    coupon_code: None
    coupon_labels: None
    date_created: datetime
    date_of_expiration: None
    expiration_date_from: None
    expiration_date_to: None
    expires: bool
    external_reference: str
    id: str
    init_point: str
    internal_metadata: None
    items: List[Metadata]
    marketplace: str
    marketplace_fee: int
    metadata: Metadata
    notification_url: None
    operation_type: str
    payer: Payer
    payment_methods: PaymentMethods
    processing_modes: None
    product_id: None
    redirect_urls: Urls
    sandbox_init_point: str
    site_id: str
    shipments: Shipments
    total_amount: None
    last_updated: None
    financing_group: str

    def __init__(self, additional_info: str, auto_return: str, back_urls: Urls, binary_mode: bool, client_id: str, collector_id: int, coupon_code: None, coupon_labels: None, date_created: datetime, date_of_expiration: None, expiration_date_from: None, expiration_date_to: None, expires: bool, external_reference: str, id: str, init_point: str, internal_metadata: None, items: List[Metadata], marketplace: str, marketplace_fee: int, metadata: Metadata, notification_url: None, operation_type: str, payer: Payer, payment_methods: PaymentMethods, processing_modes: None, product_id: None, redirect_urls: Urls, sandbox_init_point: str, site_id: str, shipments: Shipments, total_amount: None, last_updated: None, financing_group: str) -> None:
        self.additional_info = additional_info
        self.auto_return = auto_return
        self.back_urls = back_urls
        self.binary_mode = binary_mode
        self.client_id = client_id
        self.collector_id = collector_id
        self.coupon_code = coupon_code
        self.coupon_labels = coupon_labels
        self.date_created = date_created
        self.date_of_expiration = date_of_expiration
        self.expiration_date_from = expiration_date_from
        self.expiration_date_to = expiration_date_to
        self.expires = expires
        self.external_reference = external_reference
        self.id = id
        self.init_point = init_point
        self.internal_metadata = internal_metadata
        self.items = items
        self.marketplace = marketplace
        self.marketplace_fee = marketplace_fee
        self.metadata = metadata
        self.notification_url = notification_url
        self.operation_type = operation_type
        self.payer = payer
        self.payment_methods = payment_methods
        self.processing_modes = processing_modes
        self.product_id = product_id
        self.redirect_urls = redirect_urls
        self.sandbox_init_point = sandbox_init_point
        self.site_id = site_id
        self.shipments = shipments
        self.total_amount = total_amount
        self.last_updated = last_updated
        self.financing_group = financing_group

    @staticmethod
    def from_dict(obj: Any) -> 'TJSONGetProduto':
        assert isinstance(obj, dict)
        additional_info = from_str(obj.get("additional_info"))
        auto_return = from_str(obj.get("auto_return"))
        back_urls = Urls.from_dict(obj.get("back_urls"))
        binary_mode = from_bool(obj.get("binary_mode"))
        client_id = from_str(obj.get("client_id"))
        collector_id = from_int(obj.get("collector_id"))
        coupon_code = from_none(obj.get("coupon_code"))
        coupon_labels = from_none(obj.get("coupon_labels"))
        date_created = from_datetime(obj.get("date_created"))
        date_of_expiration = from_none(obj.get("date_of_expiration"))
        expiration_date_from = from_none(obj.get("expiration_date_from"))
        expiration_date_to = from_none(obj.get("expiration_date_to"))
        expires = from_bool(obj.get("expires"))
        external_reference = from_str(obj.get("external_reference"))
        id = from_str(obj.get("id"))
        init_point = from_str(obj.get("init_point"))
        internal_metadata = from_none(obj.get("internal_metadata"))
        items = from_list(Metadata.from_dict, obj.get("items"))
        marketplace = from_str(obj.get("marketplace"))
        marketplace_fee = from_int(obj.get("marketplace_fee"))
        metadata = Metadata.from_dict(obj.get("metadata"))
        notification_url = from_none(obj.get("notification_url"))
        operation_type = from_str(obj.get("operation_type"))
        payer = Payer.from_dict(obj.get("payer"))
        payment_methods = PaymentMethods.from_dict(obj.get("payment_methods"))
        processing_modes = from_none(obj.get("processing_modes"))
        product_id = from_none(obj.get("product_id"))
        redirect_urls = Urls.from_dict(obj.get("redirect_urls"))
        sandbox_init_point = from_str(obj.get("sandbox_init_point"))
        site_id = from_str(obj.get("site_id"))
        shipments = Shipments.from_dict(obj.get("shipments"))
        total_amount = from_none(obj.get("total_amount"))
        last_updated = from_none(obj.get("last_updated"))
        financing_group = from_str(obj.get("financing_group"))
        return TJSONGetProduto(additional_info, auto_return, back_urls, binary_mode, client_id, collector_id, coupon_code, coupon_labels, date_created, date_of_expiration, expiration_date_from, expiration_date_to, expires, external_reference, id, init_point, internal_metadata, items, marketplace, marketplace_fee, metadata, notification_url, operation_type, payer, payment_methods, processing_modes, product_id, redirect_urls, sandbox_init_point, site_id, shipments, total_amount, last_updated, financing_group)

    def to_dict(self) -> dict:
        result: dict = {}
        result["additional_info"] = from_str(self.additional_info)
        result["auto_return"] = from_str(self.auto_return)
        result["back_urls"] = to_class(Urls, self.back_urls)
        result["binary_mode"] = from_bool(self.binary_mode)
        result["client_id"] = from_str(self.client_id)
        result["collector_id"] = from_int(self.collector_id)
        result["coupon_code"] = from_none(self.coupon_code)
        result["coupon_labels"] = from_none(self.coupon_labels)
        result["date_created"] = self.date_created.isoformat()
        result["date_of_expiration"] = from_none(self.date_of_expiration)
        result["expiration_date_from"] = from_none(self.expiration_date_from)
        result["expiration_date_to"] = from_none(self.expiration_date_to)
        result["expires"] = from_bool(self.expires)
        result["external_reference"] = from_str(self.external_reference)
        result["id"] = from_str(self.id)
        result["init_point"] = from_str(self.init_point)
        result["internal_metadata"] = from_none(self.internal_metadata)
        result["items"] = from_list(lambda x: to_class(Metadata, x), self.items)
        result["marketplace"] = from_str(self.marketplace)
        result["marketplace_fee"] = from_int(self.marketplace_fee)
        result["metadata"] = to_class(Metadata, self.metadata)
        result["notification_url"] = from_none(self.notification_url)
        result["operation_type"] = from_str(self.operation_type)
        result["payer"] = to_class(Payer, self.payer)
        result["payment_methods"] = to_class(PaymentMethods, self.payment_methods)
        result["processing_modes"] = from_none(self.processing_modes)
        result["product_id"] = from_none(self.product_id)
        result["redirect_urls"] = to_class(Urls, self.redirect_urls)
        result["sandbox_init_point"] = from_str(self.sandbox_init_point)
        result["site_id"] = from_str(self.site_id)
        result["shipments"] = to_class(Shipments, self.shipments)
        result["total_amount"] = from_none(self.total_amount)
        result["last_updated"] = from_none(self.last_updated)
        result["financing_group"] = from_str(self.financing_group)
        return result


def tjson_get_produto_from_dict(s: Any) -> TJSONGetProduto:
    return TJSONGetProduto.from_dict(s)


def tjson_get_produto_to_dict(x: TJSONGetProduto) -> Any:
    return to_class(TJSONGetProduto, x)
