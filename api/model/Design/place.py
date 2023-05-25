from pydantic import BaseModel

class DesignPlaceBaseModel(BaseModel):
    id: int
    clothes_id: int
    name: str
    description: str
    price: float
    image: str

class DesignPlace(object):
    id = 0
    name = ""
    description = ""
    price = 0.00
    image = ""
    clothes_id = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, design_place_id, clothes_id, name, description, price, image):
        self.id = design_place_id
        self.clothes_id = clothes_id
        self.name = name
        self.price = price
        self.description = description
        self.image = image

    def asdict(self):
        return {
            "id": self.id,
            "clothes_id": self.clothes_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image
        }


def getDesignPlaces (db, design_id):
    sql = "SELECT * FROM design_to_clothes WHERE design_id=" + str(design_id)
    db.execute(sql)

    places = []

    for place in db:
        places.append(DesignPlace(int(place[7]), int(place[0]), place[4], place[11], int(place[10]), place[8]).asdict())

    return places