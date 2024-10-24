from typing import Union, List

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


class ItemWithListStr(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = []


class ItemWithSetCollection(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


class Image(BaseModel):
    url: HttpUrl
    name: str


class ItemWithImage(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None


class ItemWithCollectionPyModels(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[ItemWithCollectionPyModels]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Это приведёт к тому, что объект tags преобразуется в список, несмотря на то что тип его элементов не объявлен.

    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: ItemWithListStr):
    """
    Таким образом, в нашем примере мы можем явно указать тип данных для поля
    tags для ItemWithListStr как "список строк"
    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items3/{item_id}")
async def update_item(item_id: int, item: ItemWithSetCollection):
    """
    С помощью этого, даже если вы получите запрос с повторяющимися данными, они будут преобразованы в множество
    уникальных элементов.
    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items4/{item_id}")
async def update_item(item_id: int, item: ItemWithImage):
    """
    У каждого атрибута Pydantic-модели есть тип.
    Но этот тип может сам быть другой моделью Pydantic.
    """
    results = {"item_id": item_id, "item": item}
    return results


@app.put("/items5/{item_id}")
async def update_item(item_id: int, item: ItemWithCollectionPyModels):
    """Вы также можете использовать модели Pydantic в качестве типов вложенных в list, set и т.д"""
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers/")
async def create_offer(offer: Offer):
    """
    Заметьте, что у объекта Offer есть список объектов Item, которые, в свою очередь,
    могут содержать необязательный список объектов Image
    """
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    """
    Тела с чистыми списками элементов
    Если верхний уровень значения тела JSON-объекта представляет собой JSON array (в Python - list),
    вы можете объявить тип в параметре функции, так же, как в моделях Pydantic:
    """
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    """
    Имейте в виду, что JSON поддерживает только ключи типа str.
    Но Pydantic обеспечивает автоматическое преобразование данных.
    Это значит, что даже если пользователи вашего API могут отправлять только строки в качестве ключей, при условии,
    что эти строки содержат целые числа, Pydantic автоматический преобразует и валидирует эти данные.
    А dict, с именем weights, который вы получите в качестве ответа Pydantic, действительно будет иметь ключи типа int
    и значения типа float
    """
    return weights
