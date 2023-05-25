from pydantic import BaseModel


class ClothesBaseModel(BaseModel):
    id: int
    name: str
    price: float
    image: str
    sizes: list[str]


class Clothes(object):
    id = 0
    name = ""
    price = 0.00
    image = ""
    sizes = []

    # The class "constructor" - It's actually an initializer
    def __init__(self, clothes_id, name, price, image, size_list):
        self.id = clothes_id
        self.name = name
        self.price = price
        self.image = image
        self.sizes = size_list

    def asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "sizes": self.sizes
        }


def getClothes(db, db2, design_id):
    clothes = []

    ids = []
    sql = "SELECT * FROM design_to_clothes WHERE design_id =" + str(design_id)
    db.execute(sql)

    for item in db:
        ids.append(str(item[0]))

    sql = "SELECT * FROM clothes c WHERE clothes_id IN (" + ", ".join(ids) + ");"
    db.execute(sql)

    for item in db:
        db2.execute("SELECT * FROM clothes_to_size WHERE count > 0 AND clothes_id=" + str(item[0]))

        sizes = []

        for size in db2:
            sizes.append(size[1])

        clothes.append(Clothes(item[0], item[4], item[2], item[1], sizes).asdict())

    return clothes
