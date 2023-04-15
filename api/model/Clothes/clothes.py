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

def getClothes(db, db2):
    clothes = []

    sql = "SELECT * FROM clothes c"
    db.execute(sql)

    for item in db:
        db2.execute("SELECT * FROM clothes_to_size WHERE count > 0 AND clothes_id=" + str(item[0]))

        print(item[0])

        sizes = []

        for size in db2:
            sizes.append(size[1])

        clothes.append(Clothes(item[0], item[4], item[2], item[1], sizes).asdict())

    return clothes
