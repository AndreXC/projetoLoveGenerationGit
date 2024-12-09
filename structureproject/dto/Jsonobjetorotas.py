from typing import Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class BackUrls:
    success: str
    failure: str
    pending: str

    def __init__(self, success: str, failure: str, pending: str) -> None:
        self.success = success
        self.failure = failure
        self.pending = pending

    @staticmethod
    def from_dict(obj: Any) -> 'BackUrls':
        assert isinstance(obj, dict)
        success = from_str(obj.get("success"))
        failure = from_str(obj.get("failure"))
        pending = from_str(obj.get("pending"))
        return BackUrls(success, failure, pending)

    def to_dict(self) -> dict:
        result: dict = {}
        result["success"] = from_str(self.success)
        result["failure"] = from_str(self.failure)
        result["pending"] = from_str(self.pending)
        return result


class Item:
    pass

    def __init__(self, ) -> None:
        pass

    @staticmethod
    def from_dict(obj: Any) -> 'Item':
        assert isinstance(obj, dict)
        return Item()

    def to_dict(self) -> dict:
        result: dict = {}
        return result


class Welcome:
    items: List[Item]
    back_urls: BackUrls
    auto_return: str

    def __init__(self, items: List[Item], back_urls: BackUrls, auto_return: str) -> None:
        self.items = items
        self.back_urls = back_urls
        self.auto_return = auto_return

    @staticmethod
    def from_dict(obj: Any) -> 'Welcome':
        assert isinstance(obj, dict)
        items = from_list(Item.from_dict, obj.get("items"))
        back_urls = BackUrls.from_dict(obj.get("back_urls"))
        auto_return = from_str(obj.get("auto_return"))
        return Welcome(items, back_urls, auto_return)

    def to_dict(self) -> dict:
        result: dict = {}
        result["items"] = from_list(lambda x: to_class(Item, x), self.items)
        result["back_urls"] = to_class(BackUrls, self.back_urls)
        result["auto_return"] = from_str(self.auto_return)
        return result


def welcome_from_dict(s: Any) -> Welcome:
    return Welcome.from_dict(s)


def welcome_to_dict(x: Welcome) -> Any:
    return to_class(Welcome, x)
