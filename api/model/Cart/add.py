from typing import Union
from pydantic import BaseModel
from model.Cart.cart import CartItem
from model.Cart.get import get_cart_count
from model.Session.session import create_session, get_session_id


class AddToCartBaseModel(BaseModel):
    session_key: str
    cart_count: int


class AddToCart(object):
    session_key = ""
    cart_count = 0

    def __init__(self, session_key, cart_count):
        self.session_key = session_key
        self.cart_count = cart_count

    def asdict(self):
        return {
            "session_key": self.session_key,
            "cart_count": self.cart_count,
        }


class AddToCartBody(BaseModel):
    design: CartItem
    session_id: Union[str, None] = None


def cart_add_design(db, data: AddToCartBody):
    count = 0
    if data.session_id == '' or data.session_id is None:
        session = create_session(db)
        session_id = get_session_id(db.cursor(), session)
    else:
        session = data.session_id
        cursor = db.cursor()
        cursor.execute("UPDATE sessions SET updated_at=NOW() WHERE session_key=%s", [session])
        db.commit()
        session_id = get_session_id(db.cursor(), data.session_id)
        if session_id is None:
            session = create_session(db)
            session_id = get_session_id(db.cursor(), session)

    clothes_id = data.design.clothes_id
    design_id = data.design.design_id
    clothes_size = data.design.size
    design_place = data.design.design_place
    design_size = data.design.design_size

    cursor = db.cursor()

    sql = "INSERT INTO cart (clothes_id, clothes_to_size_id, design_id, design_size_id, count, clothes_size, session_id) VALUES (%s, %s, %s, %s, 1, %s, %s);"
    cursor.execute(sql, [str(clothes_id), str(design_place), str(design_id), str(design_size), str(clothes_size), str(session_id)])
    db.commit()

    count = get_cart_count(db.cursor(), session)

    return AddToCart(session, count).asdict()
