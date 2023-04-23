from pydantic import BaseModel

class DesignSizeBaseModel(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image: str

class DesignSize(object):
    id = 0
    name = ""
    description = ""
    price = 0.00
    image = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, design_size_id, name, description, price, image):
        self.id = design_size_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image
        }


def getDesignSizes (db, design_id):
    sql = "SELECT * FROM design_to_clothes WHERE design_id=" + str(design_id)
    db.execute(sql)

    sizes = []

    for size in db:
        sizes.append(DesignSize(int(size[7]), size[4], size[11], int(size[10]), size[8]).asdict())

    return sizes