from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class TJsonProdutosPost:
    id: str
    title: str
    quantity: int
    currency_id: str
    unit_price: int

    def __init__(self, id: str, title: str, quantity: int, currency_id: str, unit_price: float) -> None:
        self.id = id
        self.title = title
        self.quantity = quantity
        self.currency_id = currency_id
        self.unit_price = unit_price

    @staticmethod
    def from_dict(obj: Any) -> 'TJsonProdutosPost':
        assert isinstance(obj, dict)
        id = from_str(obj.get("id"))
        title = from_str(obj.get("title"))
        quantity = from_int(obj.get("quantity"))
        currency_id = from_str(obj.get("currency_id"))
        unit_price = float(obj.get("unit_price"))
        return TJsonProdutosPost(id, title, quantity, currency_id, unit_price)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(self.id)
        result["title"] = from_str(self.title)
        result["quantity"] = from_int(self.quantity)
        result["currency_id"] = from_str(self.currency_id)
        result["unit_price"] = float(self.unit_price)
        return result


def welcome_from_dict(s: Any) -> TJsonProdutosPost:
    return TJsonProdutosPost.from_dict(s)


def welcome_to_dict(x: TJsonProdutosPost) -> Any:
    return to_class(TJsonProdutosPost, x)