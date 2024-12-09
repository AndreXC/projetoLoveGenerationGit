from dataclasses import dataclass
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


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

@dataclass
class TJSONGetProdutoFinal:
    nome: str
    email: str
    mensagem: str
    service: int
    flor: str
    data: str
    hour: str
    idfotos_salvas: str
    service_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'TJSONGetProdutoFinal':
        assert isinstance(obj, dict)
        nome = from_str(obj.get("nome"))
        email = from_str(obj.get("email"))
        mensagem = from_str(obj.get("mensagem"))
        service = from_float(obj.get("service"))
        flor = from_str(obj.get("flor"))
        data = from_str(obj.get("data"))
        hour = from_str(obj.get("hour"))
        idfotos_salvas = from_str(obj.get("idfotosSalvas"))
        service_name = from_str(obj.get("serviceName"))
        return TJSONGetProdutoFinal(nome, email, mensagem, service, flor, data, hour, idfotos_salvas, service_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nome"] = from_str(self.nome)
        result["email"] = from_str(self.email)
        result["mensagem"] = from_str(self.mensagem)
        result["service"] = from_float(self.service)
        result["flor"] = from_str(self.flor)
        result["data"] = from_str(self.data)
        result["hour"] = from_str(self.hour)
        result["idfotosSalvas"] = from_str(self.idfotos_salvas)
        result["serviceName"] = from_str(self.service_name)
        return result


def tjson_get_produto_final_from_dict(s: Any) -> TJSONGetProdutoFinal:
    return TJSONGetProdutoFinal.from_dict(s)


def tjson_get_produto_final_to_dict(x: TJSONGetProdutoFinal) -> Any:
    return to_class(TJSONGetProdutoFinal, x)
