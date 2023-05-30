import uuid
from yookassa import Configuration, Payment
from pydantic import BaseModel

from config.main import yookassa_api_key, yookassa_api_shop_id
from model.Delivery.delivery import create_delivery
from model.Session.session import get_session_id
from model.Payload.payload import NewPayloadBody, create_uniq_id

Configuration.account_id = yookassa_api_shop_id
Configuration.secret_key = yookassa_api_key


class newPayment(object):
    id = str
    link = str

    def __init__(self, id, link):
        self.id = id
        self.link = link

    def asdict(self):
        return {
            "id": self.id,
            "link": self.link,
        }

def new_payment (db, data:NewPayloadBody):
    payment = Payment.create({
        "amount": {
            "value": str(data.sum),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "http://localhost:3000/cart"
        },
        "capture": True,
        "description": "Заказ №1"
    }, uuid.uuid4())

    address_sql = create_delivery(db, data.delivery)
    uniqid = create_uniq_id()

    sql = "INSERT INTO orders (" \
          "address_id, " \
          "uniq_id, " \
          "first_name, " \
          "last_name, " \
          "phone, " \
          "email, " \
          "delivery_by, " \
          "payment_code, " \
          "sum, " \
          "discount, " \
          "session_id, " \
          "delivery_price" \
      ") VALUES ((" + address_sql + "), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    cursor = db.cursor()

    cursor.execute(sql, [
        uniqid,
        data.first_name,
        data.last_name,
        data.phone,
        data.email,
        data.delivery.method,
        payment.id,
        data.sum,
        data.discount,
        get_session_id(db.cursor(), data.session_key),
        data.delivery.price
    ])

    db.commit()

    return newPayment(uniqid, payment.confirmation.confirmation_url).asdict()