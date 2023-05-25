from pydantic import BaseModel

class DesignSizeBaseModel(BaseModel):
    id: int
    name: str
    description: str
    price: float

class DesignSize(object):
    id = 0
    name = ""
    description = ""
    price = 0.00

    # The class "constructor" - It's actually an initializer
    def __init__(self, design_size_id, name, description, price):
        self.id = design_size_id
        self.name = name
        self.price = price
        self.description = description

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
        }


def getDesignSizes (db):
    sql = "SELECT * FROM design_size ORDER BY id"
    db.execute(sql)

    sizes = []

    for size in db:
        sizes.append(DesignSize(int(size[0]), size[1], size[2], int(size[3])).asdict())

    return sizes