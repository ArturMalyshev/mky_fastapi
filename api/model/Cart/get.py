from pydantic import BaseModel
from model.Session.session import update_session_date
from model.Cart.cart import Cart, CartResponse


def get_cart_count(db, session_key):
    sql = "SELECT COUNT(*) FROM cart INNER JOIN sessions s on cart.session_id = s.session_id WHERE s.session_key=%s"
    db.execute(sql, [session_key])
    for item in db:
        return item[0]


def users_cart_count(db, session_key):
    update_session_date(db, session_key)
    return CartCount(get_cart_count(db.cursor(), session_key)).asdict()


def get_cart(db, session_key):
    sql = "SELECT c.name," \
          " d.name," \
          " CONCAT (ds.size_name,' ( ',  ds.description, ' )') as design_size," \
          " dtc.position_name," \
          " cart.clothes_size," \
          " dtc.result_path," \
          " (d.design_price + c.price + ds.price + dtc.price) as price," \
          " cart.cart_id," \
          " d.design_id" \
          " FROM cart" \
          " INNER JOIN sessions s on cart.session_id = s.session_id" \
          " LEFT JOIN design d on cart.design_id = d.design_id" \
          " LEFT JOIN clothes c on cart.clothes_id = c.clothes_id" \
          " LEFT JOIN design_size ds on cart.design_size_id = ds.id" \
          " LEFT JOIN design_to_clothes dtc on cart.clothes_to_size_id = dtc.id" \
          " WHERE s.session_key=%s"
    db.execute(sql, [session_key])
    result = []
    for cart in db:
        result.append(Cart(cart[0], cart[4], cart[1], cart[2], cart[3], cart[5], cart[6], cart[7], cart[8]).asdict())
    return CartResponse(result).asdict()


class CartCountBaseModel(BaseModel):
    count: int


class CartCount(object):
    count = 0

    def __init__(self, count):
        self.count = count

    def asdict(self):
        return {
            "count": self.count,
        }
