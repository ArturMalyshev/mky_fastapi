from pydantic import BaseModel


class CartItem(BaseModel):
    design_id: int
    clothes_id: int
    design_size: int
    design_place: int
    size: str


class CartClothing(BaseModel):
    clothes_name: str
    clothes_size: str
    design_name: str
    design_size: str
    design_place: str
    design_id: int
    photo: str
    price: int
    id: int


class CartBaseModel(BaseModel):
    data: list[CartClothing]


class Cart(object):
    clothes_name = ""
    clothes_size = ""
    design_name = ""
    design_size = ""
    design_place = ""
    design_id = 0
    photo = ""
    price: 0
    id: 0

    def __init__(self, clothes_name, clothes_size, design_name, design_size, design_place, photo, price, id, design_id):
        self.clothes_name = clothes_name
        self.clothes_size = clothes_size
        self.design_name = design_name
        self.design_size = design_size
        self.design_place = design_place
        self.design_id = design_id
        self.photo = photo
        self.price = price
        self.id = id

    def asdict(self):
        return {
            "clothes_name": self.clothes_name,
            "clothes_size": self.clothes_size,
            "design_name": self.design_name,
            "design_size": self.design_size,
            "design_place": self.design_place,
            "design_id": self.design_id,
            "photo": self.photo,
            "price": self.price,
            "id": self.id
        }


class CartResponse(object):
    data = []

    def __init__(self, data):
        self.data = data

    def asdict(self):
        return {
            "data": self.data,
        }
