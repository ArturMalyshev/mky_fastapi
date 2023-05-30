from pydantic import BaseModel
from model.Session.session import get_session_id


class DropFromCartBody(BaseModel):
    cart_id: int
    session: str


def remove_from_cart(db, session_key, cart_id):
    session_id = get_session_id(db.cursor(), session_key)
    if session_id:
        sql = "DELETE FROM cart WHERE cart_id=%s AND session_id=%s"
        deleter = db.cursor()
        deleter.execute(sql, [cart_id, session_id])
        db.commit()
        return True

    return False

