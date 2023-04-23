import json
from typing import Union
from pydantic import BaseModel

from model.Clothes.clothes import ClothesBaseModel, getClothes
from model.Design.size import DesignSizeBaseModel, getDesignSizes


class DesignBaseModel(BaseModel):
    id: int
    name: str
    description: str
    image: str
    price: float
    clothes: list[ClothesBaseModel]
    size_variants: list[DesignSizeBaseModel]


class DesignPreview(BaseModel):
    id: int
    name: str
    description: Union[str, None]
    image: Union[str, None]


class Design(object):
        id = 0
        name = ""
        description = ""
        image = ""
        price = 0.00
        clothes = []
        size_variants = []

        def __init__(self, design_id, name, description, image, price=None, clothes_array=None, size_variants_array=None):
            self.id = design_id
            self.name = name
            self.description = description
            self.image = image
            self.price = price
            self.clothes = clothes_array
            self.size_variants = size_variants_array

        def asdictShort(self):
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "image": self.image
            }

        def asdict(self):
            if self.clothes is None:
                self.clothes = []
            if self.size_variants is None:
                self.size_variants = []
            if self.price is None:
                self.price = 0.00

            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "image": self.image,
                "price": self.price,
                "clothes": self.clothes,
                "size_variants": self.size_variants
            }


def get_designs_preview(db, category_id, visible:bool):
    designs = []

    sql="SELECT d.design_id, d.design_path, d.name, d.description FROM design_to_category dc INNER JOIN design d ON dc.design_id = d.design_id WHERE dc.category_id=" + str(category_id)

    if visible:
        sql += " AND d.visible=1"

    db.execute(sql)
    for design in db:
        designs.append(Design(int(design[0]), design[2], design[3], design[1]).asdictShort())

    return designs

def get_design(db1, db2, design_id, show_if_invisible:bool):
    design_clothes = getClothes(db1, db2, design_id)
    design_sizes = getDesignSizes(db1, design_id)

    sql = "SELECT * FROM design WHERE design_id=" + str(design_id)

    # if show_if_invisible is False:
    #     sql = sql + " visible=1"

    db1.execute(sql)
    result = None

    for design in db1:
        result = Design(design[0], design[2], design[3], design[1], design[4], design_clothes, design_sizes).asdict()

    return result