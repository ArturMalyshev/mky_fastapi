import json
from typing import Union
from pydantic import BaseModel

from model.Design.design import DesignPreview, get_designs_preview, Design


class Category(BaseModel):
    id: int
    parent_cat_id: Union[int, None]
    name: str
    description: Union[str, None]
    image: Union[str, None]

class CategoryResult(BaseModel):
    path: list[Category]
    catalog: list[Category]
    designs: list[DesignPreview]

class Category(object):
    id = 0
    parent_cat_id = 0
    name = ""
    description = ""
    image = ""

    def __init__(self, cat_id, parent_cat_id, name, description, image):
        self.id = cat_id
        self.parent_cat_id = parent_cat_id
        self.name = name
        self.description = description
        self.image = image

    def asdict(self):
        return {
            "id": self.id,
            "parent_cat_id": self.parent_cat_id,
            "name": self.name,
            "description": self.description,
            "image": self.image
        }

def get_category(db_connection, category_id):
    categories = []
    cat_path = []

    designs = get_designs_preview(db_connection, category_id, True)

    def get_category_path(parent_category_id):
        if parent_category_id is None:
            return
        else:
            db_connection.execute("SELECT * FROM category WHERE category_id=" + str(parent_category_id))
            for data in db_connection:
                cat_path.append(Category(data[0], data[4], data[1], data[2], data[3]).asdict())
                get_category_path(data[4])

    db_connection.execute("SELECT * FROM category WHERE category_id=" + str(category_id) + " OR parent_category_id=" + str(category_id))

    for data in db_connection:
        if data[4] == category_id:
            categories.append(Category(int(data[0]), data[4], data[1], data[2], data[3]).asdict())
        else:
            cat_path.append(Category(data[0], data[4], data[1], data[2], data[3]).asdict())

    get_category_path(cat_path[0].get("parent_cat_id"))

    return {"path": list(reversed(cat_path)), "catalog": categories , "designs": designs}

